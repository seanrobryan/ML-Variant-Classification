# ML Variant Classification (in hearing loss)

# Installation

# Environment Configuration
## Python Environment
### Create Environment
Requirements: python3.11
`python -m venv .venv`
### Activate Environment
#### MacOS/Linux
`source .venv/bin/activate`
#### Windows
##### Command Window (cmd.exe)
`.venv\Scripts\activate.bat` 
##### Powershell
`.venv\Scripts\Activate.ps1`
### Install Modules
`pip install -r requirements.txt`

# Data Acquisition
## Deafness Variation Database (DVD) variation caller format (vcf) file
TODO: Reference to publicly available DVD file
TODO: Special note for those at MORL with access to the non-public data

- DVD VCF tarball (.gz.tar)
- DVD VCF Index (.gz.tar.tbi)

## Protein Free-Folding Energy and Surface Area
TODO: Reference to Tollefson et. al. data

### Download and Process 
`./extract_otoprotein.sh`