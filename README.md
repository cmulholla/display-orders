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
Example of 3 different orders:
![example image]([http://url/to/img.png](https://private-user-images.githubusercontent.com/99295376/361945516-61eef01e-0872-4795-9f9d-6eff908c21f4.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzMzNjEyMDEsIm5iZiI6MTczMzM2MDkwMSwicGF0aCI6Ii85OTI5NTM3Ni8zNjE5NDU1MTYtNjFlZWYwMWUtMDg3Mi00Nzk1LTlmOWQtNmVmZjkwOGMyMWY0LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMDUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjA1VDAxMDgyMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTE4ZjI0NjBkMjAwOTg2M2U2OGU3NjlkMjg2NGMwYWM0NzhiYzY0YzUyNGYzNmFhYTgxNDkzZWJlMTA0YjRlYmMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.FYRqnC2TqzLwLMfrkQ7Ui2KcL_uZd8lHL-LkKN7bsuY))

This program is currently in use 24/7 at the [Neighborhood Sandwich Shack](https://neighborhoodsandwichshack.com).
