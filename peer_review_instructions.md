# peer review instructions

## Getting Started
1. download [team1.tar](https://drive.google.com/drive/folders/1dFTKt4yC9jf8F6Q1rVkyimEmZC30QbP9) and relocate the path to where the team1.tar is
2. launch the Docker app
3. type the command in terminal
    ```
    docker load < team1.tar
    docker run -p 9999:9999 team1 
    ```
4. open http://localhost:9999/

## Features
- Please check out our statistics page! There are some interesting moments when we did the annotations.
- In both Search by Title page and Search by Author page, you can search the readings based on different course topics.
  - For Type of Readings, you can choose whether they are Book, Academic Paper, or All to include both of them.
  - For Readings to Include, you can choose whether they are Require, Optional in MIT open courses, or All to include both of them.
  - Please click the Search button after making the selections.
  - If no readings appear, that means no readings match the selections. Please make other selections and try again!