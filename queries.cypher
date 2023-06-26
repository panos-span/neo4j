//1. Count all users, count all targets, count all actions:
MATCH (u:User)
RETURN count(u) AS UserCount

MATCH (t:Target)
RETURN count(t) AS TargetCount

MATCH ()-[a:ACTION]->()
RETURN count(a) AS ActionCount

//2. Show all actions (actionID) and targets (targetID) of a specific user (choose one):
MATCH (u:User {id: 0})-[a:ACTION]->(t:Target)
RETURN a.id AS ActionID, t.id AS TargetID

//3. For each user, count his/her actions:
MATCH (u:User)-[a:ACTION]->()
RETURN u.id AS UserID, count(a) AS ActionCount

//4. For each target, count how many users have done this target:
MATCH (u:User)-[a:ACTION]->(t:Target)
RETURN t.id AS TargetID, count(DISTINCT u) AS UserCount

//5. Count the average actions per user:
MATCH (u:User)-[a:ACTION]->()
RETURN (count(a) / count(DISTINCT u)) AS AverageActionsPerUser
// OR
MATCH (u:User)-[a:ACTION]->()
WITH count(a) AS Actions, count(DISTINCT u) AS Users
RETURN (Actions / Users) AS AverageActionsPerUser

//6. Show the userID and the targetID, if the action has positive Feature2:
MATCH (u:User)-[a:ACTION]->(t:Target)
  WHERE a.feature2 > 0
RETURN u.id AS UserID, t.id AS TargetID
//OR
MATCH (u:User)-[a:ACTION]->(t:Target)
  WHERE a.feature2 > 0
RETURN u.id AS UserID, t.id AS TargetID, a.feature2 AS Feature2

//7. For each targetID, count the actions with label “1”:
MATCH ()-[a:ACTION {label: 1}]->(t:Target)
RETURN t.id AS TargetID, count(a) AS ActionCount
//OR
MATCH ()-[a:ACTION {label: 1}]->(t:Target)
RETURN t.id AS TargetID, count(a) AS ActionCount
  ORDER BY ActionCount DESC
