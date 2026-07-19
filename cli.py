import argparse
import requests
import sys

API_URL = 'http://localhost:5000/inventory'


def list_items(args):
    resp = requests.get(API_URL)
    print(resp.json())


def view_item(args):
    resp = requests.get(f"{API_URL}/{args.id}")
    if resp.status_code == 200:
        print(resp.json())
    else:
        print(f"Error: {resp.text}", file=sys.stderr)


def add_item(args):
    payload = {'name': args.name, 'quantity': args.quantity}
    resp = requests.post(API_URL, json=payload)
    print(resp.json() if resp.ok else f"Error: {resp.text}")


def update_item(args):
    payload = {}
    if args.name:
        payload['name'] = args.name
    if args.quantity is not None:
        payload['quantity'] = args.quantity
    resp = requests.patch(f"{API_URL}/{args.id}", json=payload)
    print(resp.json() if resp.ok else f"Error: {resp.text}")


def delete_item(args):
    resp = requests.delete(f"{API_URL}/{args.id}")
    if resp.status_code == 204:
        print(f"Deleted item {args.id}")
    else:
        print(f"Error: {resp.text}")


def fetch_external(args):
    params = {}
    if args.barcode:
        params['barcode'] = args.barcode
    if args.name:
        params['name'] = args.name
    resp = requests.get(f"{API_URL}/fetch", params=params)
    print(resp.json() if resp.ok else f"Error: {resp.text}")


def main():
    parser = argparse.ArgumentParser(description='Inventory CLI')
    sub = parser.add_subparsers()

    p = sub.add_parser('list')
    p.set_defaults(func=list_items)

    p = sub.add_parser('view')
    p.add_argument('id', type=int)
    p.set_defaults(func=view_item)

    p = sub.add_parser('add')
    p.add_argument('--name', required=True)
    p.add_argument('--quantity', type=int, default=0)
    p.set_defaults(func=add_item)

    p = sub.add_parser('update')
    p.add_argument('id', type=int)
    p.add_argument('--name')
    p.add_argument('--quantity', type=int)
    p.set_defaults(func=update_item)

    p = sub.add_parser('delete')
    p.add_argument('id', type=int)
    p.set_defaults(func=delete_item)

    p = sub.add_parser('fetch')
    p.add_argument('--barcode')
    p.add_argument('--name')
    p.set_defaults(func=fetch_external)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()