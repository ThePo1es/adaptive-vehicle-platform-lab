from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import stat
import subprocess
import tarfile
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import TypedDict, cast, override


class ManifestEntry(TypedDict):
    url: str
    filename: str
    sha256: str
    dumpmachine: str
    dumpfullversion: str


class Manifest(TypedDict):
    release: str
    platforms: dict[str, ManifestEntry]


@dataclass(frozen=True, slots=True)
class ProvisionError(Exception):
    reason: str

    @override
    def __str__(self) -> str:
        return self.reason


@dataclass(frozen=True, slots=True)
class ProvisionedGnu:
    compiler: Path
    archive: Path
    digest: str
    version: str
    machine: str


def read_entry(manifest_path: Path) -> ManifestEntry:
    manifest = cast(Manifest, json.loads(manifest_path.read_text(encoding="utf-8")))
    if manifest.get("release") != "14.3.Rel1":
        raise ProvisionError("GNU manifest release must be 14.3.Rel1")
    key = f"{'windows' if os.name == 'nt' else 'linux'}-{platform.machine().lower()}"
    try:
        return manifest["platforms"][key]
    except KeyError as error:
        raise ProvisionError(f"unsupported GNU host platform: {key}") from error


def verify_archive(archive: Path, entry: ManifestEntry) -> str:
    if archive.name != entry["filename"]:
        raise ProvisionError(f"unsupported GNU archive name: {archive.name}")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != entry["sha256"]:
        raise ProvisionError(
            f"GNU archive SHA-256 mismatch: observed={digest} expected={entry['sha256']}"
        )
    return digest


def _check_name(name: str) -> None:
    path = PurePosixPath(name.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts:
        raise ProvisionError(f"unsafe GNU archive member: {name}")


def _extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    if archive.suffix == ".zip":
        with zipfile.ZipFile(archive) as bundle:
            for member in bundle.infolist():
                _check_name(member.filename)
                if stat.S_IFMT(member.external_attr >> 16) == stat.S_IFLNK:
                    raise ProvisionError(f"GNU archive symlink is not allowed: {member.filename}")
            bundle.extractall(destination)
        return
    with tarfile.open(archive, mode="r:xz") as bundle:
        for member in bundle.getmembers():
            _check_name(member.name)
            if not (member.isfile() or member.isdir() or member.issym() or member.islnk()):
                raise ProvisionError(f"GNU archive special member is not allowed: {member.name}")
        bundle.extractall(destination, filter="data")


def _compiler(extract_root: Path) -> Path:
    name = "arm-none-eabi-gcc.exe" if os.name == "nt" else "arm-none-eabi-gcc"
    matches = tuple(path for path in extract_root.rglob(name) if path.parent.name == "bin")
    if len(matches) != 1:
        raise ProvisionError(f"verified GNU archive must contain exactly one {name}")
    candidate = matches[0]
    root = extract_root.resolve(strict=True)
    current = extract_root
    for part in candidate.relative_to(extract_root).parts:
        current /= part
        if current.is_symlink():
            raise ProvisionError("GNU compiler path must not contain symlinks")
    compiler = candidate.resolve(strict=True)
    if not compiler.is_relative_to(root):
        raise ProvisionError("GNU compiler must be a nonsymlink inside the verified extraction")
    return compiler


def compiler_environment() -> dict[str, str]:
    environment = os.environ.copy()
    for name in (
        "GCC_EXEC_PREFIX", "COMPILER_PATH", "LIBRARY_PATH", "CPATH",
        "C_INCLUDE_PATH", "CPLUS_INCLUDE_PATH", "DEPENDENCIES_OUTPUT",
    ):
        _ = environment.pop(name, None)
    return environment


def _download(entry: ManifestEntry, archive: Path) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    partial = archive.with_suffix(archive.suffix + ".partial")
    try:
        downloaded, _headers = urllib.request.urlretrieve(entry["url"], partial)
        if Path(downloaded) != partial:
            raise ProvisionError(f"GNU archive download wrote an unexpected path: {downloaded}")
        _ = partial.replace(archive)
    finally:
        partial.unlink(missing_ok=True)


def provision(manifest_path: Path, cache: Path, *, download: bool) -> ProvisionedGnu:
    entry = read_entry(manifest_path)
    root = cache / entry["sha256"]
    archive = root / entry["filename"]
    if not archive.is_file():
        if not download:
            raise ProvisionError("verified GNU archive is absent; run the pinned provisioner")
        _download(entry, archive)
    digest = verify_archive(archive, entry)
    extract_root = root / "extract"
    marker = root / "verified.sha256"
    if not extract_root.is_dir() or not marker.is_file() or marker.read_text().strip() != digest:
        if extract_root.exists():
            shutil.rmtree(extract_root)
        _extract(archive, extract_root)
        _ = marker.write_text(digest + "\n", encoding="ascii")
    compiler = _compiler(extract_root)
    environment = compiler_environment()
    machine = subprocess.run(
        [str(compiler), "-dumpmachine"], env=environment, check=True, capture_output=True, text=True
    ).stdout.strip()
    version = subprocess.run(
        [str(compiler), "-dumpfullversion"], env=environment, check=True, capture_output=True, text=True
    ).stdout.strip()
    if machine != entry["dumpmachine"] or version != entry["dumpfullversion"]:
        raise ProvisionError(f"GNU identity mismatch: machine={machine} version={version}")
    return ProvisionedGnu(compiler, archive, digest, version, machine)
