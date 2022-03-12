Python client library to interact with Farcaster ABI.

Build the image;
docker build -t farcaster-python .

Run the image (make sure to set the env variable to your Rinkeby network addres);
docker run -e RINKEBY_NETWORK_ADDR="[XXXX]" --rm farcaster-python