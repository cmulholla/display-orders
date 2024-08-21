# Summary
This is a small python program which runs in the background of an order taking computer, waits for updates to a .txt file, calculates the current orders, then prints them to the console.

Functionality:
- create <customer_name> <list of orders>
- modify <customer_name> <overwritten order>
- pay <customer_name>
  - Displays (paid) next to the user's name. If called more than once, it will be added to their order.
- delete <customer_name>

Example orders.txt file:
```
create Alfred_1 ['Mayda', 'Elricia', 'Kathlma']
delete Alfred_1
create Mildred_2 ['Jesus', 'Ceron', 'Mary']
create Rachal_3 ['Man', 'Isiahorothy', 'Donnemy']
modify Mildred_2 ['Jesus', 'Ceron', 'Mary', 'Jennores', 'Ashssie', 'Beny']
pay Mildred_2
delete Mildred_2
```

# Future Updates
- Chrome UI
