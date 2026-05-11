# About : 
- path traversal
- directory fuzzing
- ...

# Interesting
1. got response code `200` at some paths like **../api/admin** but the page html shows a `404 not found`
\
Why : 
- the server tries to hide the path
- try to analyse it
2. 