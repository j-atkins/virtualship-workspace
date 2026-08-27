# VirtualShip Post-processing Binder

The VirtualShip Post-processing Binder is a repository dedicated to hosting a VirtualShip workspace. It provides a convenient environment for users to run and interact with VirtualShip post-processing tools and tutorials.

Instead of hard-coding the contents of the workspace into the repository, this Binder setup fetches the necessary files from the VirtualShip GitHub repository at runtime. This approach ensures that users always have access to the latest versions of the tutorials and tools without needing to update the Binder repository itself.

The workflow should flag issues fetching the relevant files (e.g. their file paths have changed or they have been deleted) and alert the user to the issue, and request that they raise an issue on the VirtualShip GitHub repository.

To add any new files to the workspace, simply add their paths to the `.binder/files_to_fetch.txt` file. The postBuild script will automatically fetch these files when the Binder environment is built.