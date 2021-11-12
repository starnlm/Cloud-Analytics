This folder contains files used to collect data from bigTwitter.json and store it onto couchDB on MRC.
1. The extractor.py and reduceTweets.py files run on Spartan as that is a lot faster compared to local procecssing
2. Use sbatch spartan.slurm, spartan2.slurm to run these files in the respective order.
3. The file obtained from this operation needs to be downloaded and uploaded to the MRC instance along with transferFinal.py. This will transfer all the tweets to the couchDB database.
4. This is only a one-time process and doesn't need to run more than once!
