# Sideproject Management

_my ongoing attempt to get a grip on my sprawling mass of sideprojects_


- **Check the [guidelines](guidelines/general.md)!**


## Utils

### Make Missing Notes For GH Repos

- makes a very basic markdown note for every repo of mine
- make sure to install `requirements.txt` and set `.env` according to `.demo-env`


### Mock Folder Structure Documentation

A little shell script mocking a formatted list of the folder structure in a project so you can add comments to important files and directories.

Recommended to add into `.bashrc` like: 

```sh
alias document_folder_structure='bash ~/GITHUB/sideproject-management/utils/mock_folder_structure_documentation_in_md.sh'
```

### Update Note Metadata Based on GH Repo Data

- goes through all the md notes in the Obs folder of sideprojects
- puts in github-based data, currently stars and archival status


- *very slow*
  - would be worth putting in autostart, only yeah, takes like 90 seconds to run
    - ...and it's not like some archived private project would _change_, so that's kind of stupid to run every bootup