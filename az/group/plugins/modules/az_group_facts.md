# Example usage

```yaml
  - name: Get Azure Group facts
    az.group.az_group_facts:
      subscription: "Pay-As-You-Go"
```

# Output

```json
ok: [localhost] => {
    "msg": {
        "ansible_facts": {
            "groups": [
                "test1",
                "NetworkWatcherRG",
                "Meggitt"
            ]
        },
        "changed": false,
        "failed": false
    }
}
```