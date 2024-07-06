# How to use


## Load data

Having a file `people.csv` with the following format:

```csv
Zachary Bowman,CEO,CEO,jasonsmith@miller.net
Hayley Allen MD,Engineering,Marketing Specialist,timothyortiz@moore.com
Margaret Kane,Finance,Financial Analyst,juliemay@white-hamilton.biz
Jodi Jackson,Customer Support,Sales Representative,smithsharon@gmail.com
Kathy Rice MD,Engineering,Product Manager,lswanson@coleman.biz
Marie King,Marketing,HR Manager,wtaylor@hotmail.com
Jessica Cross,Marketing,Financial Analyst,clee@hotmail.com
David Perez,Engineering,HR Manager,rita14@gmail.com
Jack Jones,Finance,Financial Analyst,nancy94@gmail.com
Ryan Anthony,Sales,Product Manager,ubaker@gmail.com
Amy Webb,Marketing,Financial Analyst,littlebenjamin@logan.org
Thomas Espinoza,Engineering,HR Manager,barrerasamantha@shaw-waller.com
...
```

Run `dundie load` command

```py
dundie load people.csv
```

## Viewing data

### Viewing all information

```bash
$ dundie show
Initializing dundie ...............
                                       Dunder Mifflin Report
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Email           ┃ Balance ┃ Last_Movement   ┃ Name            ┃ Dept           ┃ Role            ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ jasonsmith@mil… │ 500     │ 2024-07-04T10:… │ Zachary Bowman  │ CEO            │ CEO             │
│ timothyortiz@m… │ 500     │ 2024-07-04T10:… │ Hayley Allen MD │ Engineering    │ Marketing       │
│                 │         │                 │                 │                │ Specialist      │
│ juliemay@white… │ 500     │ 2024-07-04T10:… │ Margaret Kane   │ Finance        │ Financial       │
│                 │         │                 │                 │                │ Analyst         │
│ smithsharon@gm… │ 500     │ 2024-07-04T10:… │ Jodi Jackson    │ Customer       │ Sales           │
│                 │         │                 │                 │ Support        │ Representative  │
│ lswanson@colem… │ 500     │ 2024-07-04T10:… │ Kathy Rice MD   │ Engineering    │ Product Manager │
│ wtaylor@hotmai… │ 500     │ 2024-07-04T10:… │ Marie King      │ Marketing      │ HR Manager      │
│ clee@hotmail.c… │ 500     │ 2024-07-04T10:… │ Jessica Cross   │ Marketing      │ Financial       │
│                 │         │                 │                 │                │ Analyst         │
│ rita14@gmail.c… │ 500     │ 2024-07-04T10:… │ David Perez     │ Engineering    │ HR Manager      │
│ nancy94@gmail.… │ 500     │ 2024-07-04T10:… │ Jack Jones      │ Finance        │ Financial       │
│                 │         │                 │                 │                │ Analyst         │
│ ubaker@gmail.c… │ 494     │ 2024-07-04T14:… │ Ryan Anthony    │ Sales          │ Product Manager │
│ littlebenjamin… │ 500     │ 2024-07-04T10:… │ Amy Webb        │ Marketing      │ Financial       │
```

### Filtering

Available filters are `--dept` and `--email`

```bash
dundie show --dept=Sales
Initializing dundie ...............
                                       Dunder Mifflin Report
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Email              ┃ Balance ┃ Last_Movement      ┃ Name             ┃ Dept  ┃ Role              ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ ubaker@gmail.com   │ 494     │ 2024-07-04T14:22:… │ Ryan Anthony     │ Sales │ Product Manager   │
│ garciakristina@ya… │ 494     │ 2024-07-04T14:22:… │ Jennifer Wilson  │ Sales │ Financial Analyst │
│ hannah97@tucker.n… │ 494     │ 2024-07-04T14:22:… │ Dalton Donaldson │ Sales │ Financial Analyst │
│ coreyjones@chandl… │ 494     │ 2024-07-04T14:22:… │ Corey Ellis      │ Sales │ Customer          │
│                    │         │                    │                  │       │ Specialist        │
│ williamswilliam@w… │ 494     │ 2024-07-04T14:22:… │ Kelly Romero     │ Sales │ HR Manager        │
│ wilsontodd@mason.… │ 494     │ 2024-07-04T14:22:… │ Adrian Leblanc   │ Sales │ Product Manager   │
│ daviskatherine@ya… │ 494     │ 2024-07-04T14:22:… │ Edward Brown     │ Sales │ Product Manager   │
│ vsweeney@green-wa… │ 494     │ 2024-07-04T14:22:… │ Kelly Long       │ Sales │ Marketing         │
│                    │         │                    │                  │       │ Specialist        │
│ ediaz@gmail.com    │ 494     │ 2024-07-04T14:22:… │ Kyle Rodriguez   │ Sales │ Marketing         │
│                    │         │                    │                  │       │ Specialist        │
│ patriciaanderson@… │ 494     │ 2024-07-04T14:22:… │ Amy Bailey       │ Sales │ Financial Analyst │
│ nreed@yahoo.com    │ 494     │ 2024-07-04T14:22:… │ Oscar Flynn      │ Sales │ HR Manager        │
```

> **NOTE** passing `--output=file.json` will save a json file with the results.

## Adding points

An admin user can easily add points to any user or dept.

```bash
dundie add 100 --email=maustin@yahoo.com
Initializing dundie ...............
                                       Dunder Mifflin Report
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Email             ┃ Balance ┃ Last_Movement            ┃ Name        ┃ Dept  ┃ Role              ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ maustin@yahoo.com │ 594     │ 2024-07-04T23:09:05.959… │ Chelsea Lee │ Sales │ Financial Analyst │
└───────────────────┴─────────┴──────────────────────────┴─────────────┴───────┴───────────────────┘

```

Available selectors are `--email` and `--dept`
