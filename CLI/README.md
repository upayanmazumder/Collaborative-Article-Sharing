# Collaborative-Article-Sharing CLI

A Command-Line Interface (CLI) tool for interacting with the [Collaborative-Article-Sharing](https://github.com/upayanmazumder/Collaborative-Article-Sharing) project.

### Available Commands

> For a full comprehensive list, use the help command

- **`cas info`**  
  Displays project and developer information.

- **`cas help`**  
  Shows the help article for available commands.

- **`cas auth`**  
  Initiates the authentication process.

- **`cas push <article-link> [-m <message>]`**  
  Adds an article with an optional message.

- **`cas pull`**  
  Retrieves your saved articles.

- **`cas group:create`**
  Create a group

- **`cas group:delete`**
  Delete a group

- **`cas group:privacy`**
  Change a group's privacy settings

- **`cas group:list`**
  Get the list of public groups

### Development

To run the CLI tool, first navigate to the CLI folder using the command:

```sh
cd /d:/upayanmazumder/Collaborative-Article-Sharing/CLI
```

Then, execute the following command to start the CLI:

```sh
pip install -e .
```

Once build completes, use the `cas` command
