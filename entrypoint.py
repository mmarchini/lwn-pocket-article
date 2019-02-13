import get_pocket_token, lwn_to_pocket
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--get-pocket-token', action='store_true',
                    help='Get the Pocket Token from OAuth')

args = parser.parse_args()
if args.get_pocket_token:
  get_pocket_token.main()
else:
  lwn_to_pocket.main()
