### => Relative import path (import all CLI module)
#from dundie import cli

### => Relative import path (all at same directory)
#from .cli import main

### => ABSOLUTE import path
from dundie.cli import main

if __name__ == "__main__":
    main()
