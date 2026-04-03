import argparse
import asyncio
import json
import sys
from typing import Any, Optional

from wElasticsearch import WElasticsearch, QueryBuilder, __version__


def create_client(args: argparse.Namespace) -> WElasticsearch:
    kwargs: dict[str, Any] = {"hosts": args.hosts}
    if args.username and args.password:
        kwargs["username"] = args.username
        kwargs["password"] = args.password
    if args.api_key:
        parts = args.api_key.split(":")
        if len(parts) == 2:
            kwargs["api_key"] = (parts[0], parts[1])
    return WElasticsearch(**kwargs)


async def cmd_index_create(args: argparse.Namespace, client: WElasticsearch) -> int:
    mappings = json.loads(args.mappings) if args.mappings else None
    settings = json.loads(args.settings) if args.settings else None
    aliases = json.loads(args.aliases) if args.aliases else None
    result = await client.index.create_index_async(
        args.index,
        mappings=mappings,
        settings=settings,
        aliases=aliases,
        exist_ok=args.force,
    )
    print(json.dumps(result, indent=2))
    return 0


async def cmd_index_delete(args: argparse.Namespace, client: WElasticsearch) -> int:
    result = await client.index.delete_index_async(
        args.index, ignore_missing=args.force
    )
    print(json.dumps(result, indent=2))
    return 0


async def cmd_index_exists(args: argparse.Namespace, client: WElasticsearch) -> int:
    exists = await client.index.exists_async(args.index)
    print(json.dumps({"exists": exists}))
    return 0


async def cmd_index_list(args: argparse.Namespace, client: WElasticsearch) -> int:
    indices = await client.index.list_indices_async()
    print(json.dumps(indices, indent=2))
    return 0


async def cmd_index_mapping(args: argparse.Namespace, client: WElasticsearch) -> int:
    mapping = await client.index.get_mapping_async(args.index)
    print(json.dumps(mapping, indent=2))
    return 0


async def cmd_doc_index(args: argparse.Namespace, client: WElasticsearch) -> int:
    doc = json.loads(args.document)
    result = await client.index_document_async(args.index, doc, id=args.id)
    print(json.dumps(result, indent=2))
    return 0


async def cmd_doc_get(args: argparse.Namespace, client: WElasticsearch) -> int:
    result = await client.get_document_async(args.index, args.id)
    print(json.dumps(result, indent=2))
    return 0


async def cmd_doc_delete(args: argparse.Namespace, client: WElasticsearch) -> int:
    result = await client.delete_document_async(args.index, args.id)
    print(json.dumps(result, indent=2))
    return 0


async def cmd_search(args: argparse.Namespace, client: WElasticsearch) -> int:
    query = json.loads(args.query) if args.query else None
    result = await client.search_async(
        args.index, query, from_=args.from_, size=args.size
    )
    print(json.dumps(result, indent=2))
    return 0


async def cmd_query(args: argparse.Namespace, client: WElasticsearch) -> int:
    builder = QueryBuilder()
    if args.match_all:
        builder.match_all()
    elif args.term:
        parts = args.term.split("=", 1)
        if len(parts) == 2:
            builder.term(parts[0], parts[1])
    elif args.match:
        parts = args.match.split("=", 1)
        if len(parts) == 2:
            builder.match(parts[0], parts[1])
    result = await client.search_async(
        args.index, builder.build(), from_=args.from_, size=args.size
    )
    print(json.dumps(result, indent=2))
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="wElasticsearch", description="Elasticsearch ORM CLI"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--hosts", default="http://localhost:9200", help="Elasticsearch hosts"
    )
    parser.add_argument("--username", help="Username for basic auth")
    parser.add_argument("--password", help="Password for basic auth")
    parser.add_argument("--api-key", help="API key (format: id:api_key)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    p_index = subparsers.add_parser("index", help="Index management")
    subparsers_index = p_index.add_subparsers(dest="subcommand", required=True)

    cmd_create = subparsers_index.add_parser("create", help="Create an index")
    cmd_create.add_argument("index", help="Index name")
    cmd_create.add_argument("--mappings", help="Index mappings (JSON)")
    cmd_create.add_argument("--settings", help="Index settings (JSON)")
    cmd_create.add_argument("--aliases", help="Index aliases (JSON)")
    cmd_create.add_argument("--force", action="store_true", help="Ignore if exists")

    cmd_delete = subparsers_index.add_parser("delete", help="Delete an index")
    cmd_delete.add_argument("index", help="Index name")
    cmd_delete.add_argument("--force", action="store_true", help="Ignore if not exists")

    cmd_exists = subparsers_index.add_parser("exists", help="Check if index exists")
    cmd_exists.add_argument("index", help="Index name")

    cmd_list = subparsers_index.add_parser("list", help="List indices")
    cmd_mapping = subparsers_index.add_parser("mapping", help="Get index mapping")
    cmd_mapping.add_argument("index", help="Index name")

    p_doc = subparsers.add_parser("doc", help="Document operations")
    subparsers_doc = p_doc.add_subparsers(dest="subcommand", required=True)

    cmd_doc_index = subparsers_doc.add_parser("index", help="Index a document")
    cmd_doc_index.add_argument("index", help="Index name")
    cmd_doc_index.add_argument("document", help="Document (JSON)")
    cmd_doc_index.add_argument("--id", help="Document ID")

    cmd_doc_get = subparsers_doc.add_parser("get", help="Get a document")
    cmd_doc_get.add_argument("index", help="Index name")
    cmd_doc_get.add_argument("id", help="Document ID")

    cmd_doc_delete = subparsers_doc.add_parser("delete", help="Delete a document")
    cmd_doc_delete.add_argument("index", help="Index name")
    cmd_doc_delete.add_argument("id", help="Document ID")

    p_search = subparsers.add_parser("search", help="Search documents")
    p_search.add_argument("index", help="Index name")
    p_search.add_argument("--query", help="Query (JSON)")
    p_search.add_argument("--from", type=int, default=0, dest="from_")
    p_search.add_argument("--size", type=int, default=10)

    p_query = subparsers.add_parser("query", help="Simple query builder")
    p_query.add_argument("index", help="Index name")
    p_query.add_argument("--match-all", action="store_true")
    p_query.add_argument("--term", help="Term query (field=value)")
    p_query.add_argument("--match", help="Match query (field=value)")
    p_query.add_argument("--from", type=int, default=0, dest="from_")
    p_query.add_argument("--size", type=int, default=10)

    args = parser.parse_args()
    client = create_client(args)

    commands = {
        ("index", "create"): cmd_index_create,
        ("index", "delete"): cmd_index_delete,
        ("index", "exists"): cmd_index_exists,
        ("index", "list"): cmd_index_list,
        ("index", "mapping"): cmd_index_mapping,
        ("doc", "index"): cmd_doc_index,
        ("doc", "get"): cmd_doc_get,
        ("doc", "delete"): cmd_doc_delete,
        ("search", None): cmd_search,
        ("query", None): cmd_query,
    }

    key = (
        (args.command, args.subcommand)
        if hasattr(args, "subcommand")
        else (args.command, None)
    )
    cmd = commands.get(key)

    if cmd:
        try:
            if asyncio.iscoroutinefunction(cmd):
                exit_code = asyncio.run(cmd(args, client))
            else:
                exit_code = cmd(args, client)
            sys.exit(exit_code)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            asyncio.run(client.close_async())
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
