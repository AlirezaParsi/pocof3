rm -rf KernelSU-Next
curl -LSs "https://raw.githubusercontent.com/rifsxd/KernelSU-Next/next/kernel/setup.sh" | bash -s next
cp -rf "0001-Implement-SUSFS-v1.5.3-universal.patch" KernelSU-Next && patch -p1 < "./KernelSU-Next/0001-Implement-SUSFS-v1.5.3-universal.patch" -y
