# DPIA Summary

## Purpose

This document summarises the Data Protection Impact Assessment for the use of Swedish
register data in the Mobilitetsmodellen research project.

## Processing Description

- **Data controller**: Department of Economics, Stockholm University.
- **Data processor**: Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom Imanov.
- **Personal data categories**: Person identifiers (pseudonymised PIDs), income records,
  education, occupation, municipality codes, birth year, parent-child links.
- **Data subjects**: Swedish residents born 1940-2000 present in Flergenerationsregistret.
- **Legal basis**: Art. 6(1)(e) + 9(2)(j) GDPR; Etikprövningslagen 2003:460.
- **Processing environment**: SCB MONA/SAFE; no export of personal data.

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Re-identification via linkage | Low | High | Pseudonymisation; MONA/SAFE environment |
| Unauthorised access | Low | High | SCB MONA access controls; gitleaks |
| Output disclosure | Low | Medium | Cell suppression; aggregate publication only |

## Outcome

Residual risk is acceptable given SCB MONA/SAFE safeguards. Processing may proceed
subject to ethics approval from Etikprövningsmyndigheten.

## Note on This Repository

This repository contains only synthetic data. The DPIA applies to production use with
real register data accessed under MONA/SAFE authorisation.
