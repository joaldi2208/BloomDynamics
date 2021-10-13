# BloomDynamics
Observations of bloom dynamics in the Bornholm Basin from gliders

## Instructions for using Git

### Download Repository
Clone the repository to your personal computer. 
The following command will create an folder named BloomDynamics.
```
git clone https://github.com/joaldi2208/BloomDynamics
```
This is only needed at the beginning!

### Upload Changes
After finishing your changes (end of the workday) upload your changes.
```
git add filesYouChanged
git commit -m "short message what you did"
git push
```
It can happen that `git push` ask for your username and password. 
The Username is your GitHub username. The password is **NOT** your password. 
Go to GitHub and go to *setting* right below your profil photo (top right corner).
Then go the *developer setting* and *personal access tokens*. 
You can find *Generate new token* on the top. Allow at least the *repo* section.
Take the generated token and use this as password. Now you should be able to push your changes.

### Get latest Version
On the next day you should be on the latest stand. Therefore use following command.
```
git pull
```
Now your folder should be updated.

