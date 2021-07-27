---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behaviour, including error message if any.

**Expected behaviour**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Desktop/Server/Device (please complete the following information):**
 - Device used to run the Custom Component [e.g. Raspberry Pi, NUC]
 - Method of installation [e.g. via HACS or manual]
 - Version of the Custom Component installed?
 - Model of the Current Cost Device

**Additional context**
Add any other context about the problem here.

**Logs**
Please set the Current Cost Custom Component's logging level to debug and provide relevant logs section from Home-Assistant.
To Enable debug logging level, add this to your configuration.yaml and restart:

```
logger:
  default: error
  logs:
    custom_components.currentcost: debug
```
