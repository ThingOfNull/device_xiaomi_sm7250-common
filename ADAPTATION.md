# SM7250 common tree — Android 16 / 4.19 vendor kernel adaptation

Common device tree for Xiaomi SM7250 devices (used by **vangogh**), adapted to
run **LineageOS 23.2 (Android 16)** on the **4.19 vendor kernel**.

## Branch

- `lineage-23.2-4.19` — Android 16 (LineageOS 23.2) + 4.19 vendor kernel.
- `main` mirrors it.

Related repositories:

- [device_xiaomi_vangogh](https://github.com/ThingOfNull/device_xiaomi_vangogh)
- [kernel_xiaomi_sm7250](https://github.com/ThingOfNull/kernel_xiaomi_sm7250) — branch `lineage-23.2-4.19`

## Changes for this adaptation

- **BoardConfigCommon**: build the kernel from `kernel/xiaomi/sm7250` with the
  full 4.19.325 configuration (`vangogh_419_defconfig`); reuse the 4.19 vendor
  display/camera/audio HALs; 64-bit-only userspace.
- **LiveDisplay / colours**: keep the DM/QDCM raw mode list disabled
  (`soong_config_set_bool,livedisplay_sdm,enable_dm,false`) so Settings shows
  the four AOSP colour modes (Natural / Boosted / Saturated / Adaptive), which
  go through SurfaceFlinger/HWC; picture adjustment (PA) stays enabled.
- **XiaomiParts (doze/AOD)**: enable `DozeSettingsActivity` (declared disabled
  upstream) and export it so Settings → Display → Ambient display opens the
  device doze page; make the doze help dialog a `public static` fragment
  (fixes the first-open crash); hide sensor categories that do not exist on
  this device and do not crash when the SystemUI proximity bool is missing.
- **Display/Touch**: ship the FocalTech touch IDC configuration
  (`idc/fts_ts.idc`) used by the vendor touch driver.
- **Vendor blobs**: add the LTM/QDCM calibration XMLs required by the vendor
  composer and the DPPS canary patch (`proprietary-files.txt`,
  `tools/patch-libdpps.py`).
- **Sepolicy / fstab / init**: 4.19 bring-up fixes (UFS, dm, keymaster, USB,
  early adb, etc.). The kernel-side counterpart lives in the kernel repository.

## Build

```bash
source build/envsetup.sh
lunch lineage_vangogh-bp4a-userdebug
mka bacon
```

See the device tree README for the full device specification and the kernel
repository README for the kernel build details.

## Status / known issues

Working on the 4.19 kernel (Android 16 / LineageOS 23.2): boot, display
(DSI/DRM), touch, Wi-Fi, audio, charging, in-display fingerprint, AOD (kernel +
Settings entry), the four AOSP colour modes and OTA updates.

Known limitations:

- The OTA is signed with the AOSP test keys; re-sign with your own keys before
  production distribution.
- Recovery adb is authenticated by default (`ro.adb.secure=1`); authorize it
  from the recovery UI or rebuild with it disabled if you need unattended adb.
- LiveDisplay picture-adjustment values are global (per-QDCM-mode storage
  degrades to mode 0 because the raw mode list is disabled).
- Colour-mode differences can be subtle on some panels; the framework/HWC
  state changes are the source of truth.
- The vendor composer needs the LTM/QDCM XMLs and the patched DPPS blob from
  this tree; do not replace the vendor image without them.
- The 5.10 kernel port is experimental and maintained separately; it is not
  part of this 4.19 release.
