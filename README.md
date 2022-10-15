Task:

Write a Python script that will collect the address from the site in all cities (city, street, house number, etc.), coordinates, working hours (if any) (decomposed by days) and telephones (general and additional, if indicated).

Description:

Description: The script must generate a json file that will store the array objects Exclude use of selenium,json file format:

[
{
 "address": "Bernardo O Higgins 479 - San Fernando",
 "latlon": [-70.98583, -34.589468],
 "name": "Oriencoop",
 "phones": [ "72201048", "600 200 0015", "+56712207838"]
 "working_hours": ["mon-thu 8:50 - 14:10 15:00-17:10", "fri 8:50 - 14:10
15:00-17:10"]
 },
...
]