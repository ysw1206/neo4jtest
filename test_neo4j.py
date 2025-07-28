from neo4j import GraphDatabase
import os

URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
USER = os.getenv('NEO4J_USER', 'neo4j')
PASSWORD = os.getenv('NEO4J_PASSWORD', 'test')

class Neo4jExample:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def create_nodes_and_relationships(self):
        with self.driver.session() as session:
            session.run("CREATE (:Module {name: 'A'})")
            session.run("CREATE (:Module {name: 'B'})")
            session.run("CREATE (:Function {name: 'foo'})")
            session.run("CREATE (:Module {name: 'C'})")
            session.run(
                "MATCH (a:Module {name:'A'}), (b:Module {name:'B'}) "
                "CREATE (a)-[:IMPORTS]->(b)"
            )
            session.run(
                "MATCH (c:Module {name:'C'}), (a:Module {name:'A'}) "
                "CREATE (c)-[:IMPORTS]->(a)"
            )
            session.run(
                "MATCH (b:Module {name:'B'}), (f:Function {name:'foo'}) "
                "CREATE (b)-[:DECLARES]->(f)"
            )

    def query_connected_to_a(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (a:Module {name: 'A'})--(n) RETURN n.name as name, labels(n) as labels"
            )
            return [(record['name'], record['labels']) for record in result]

def main():
    app = Neo4jExample(URI, USER, PASSWORD)
    try:
        print("Clearing database...")
        app.clear()
        print("Creating nodes and relationships...")
        app.create_nodes_and_relationships()
        print("Nodes connected to Module A:")
        for name, labels in app.query_connected_to_a():
            print(f" - {name} ({', '.join(labels)})")
    finally:
        app.close()

if __name__ == '__main__':
    main()
