# Example

```yaml
  - name: Get VM facts
    az.compute.az_vm_facts:
      vm: vm1
      group: test1
```

# Output


```json
ok: [localhost] => {
    "msg": {
        "ansible_facts": {
            "data_disks": [],
            "nics": [
                "/subscriptions/adc61b44-af20-4d50-80c9-40fda8b6c177/resourceGroups/test1/providers/Microsoft.Network/networkInterfaces/vm1VMNic"
            ],
            "os_disk": "vm1_OsDisk_1_46bf3cd8f1974d75a0aaf4a59c14b995"
        },
        "changed": false,
        "failed": false
    }
}
```