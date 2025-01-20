import networkx as nx
import matplotlib.pyplot as plt
import sys
sys.stdout.reconfigure(encoding='utf-8')



def build_graph():
    # Створюємо орієнтований граф
    G = nx.DiGraph()

    # Додаємо ребра із пропускними здатностями
    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]

    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)

    return G


def compute_max_flow(G, sources, sinks):
    # Додаємо уявне джерело та стік
    super_source = "Джерело"
    super_sink = "Стік"

    for source in sources:
        G.add_edge(super_source, source, capacity=float('inf'))

    for sink in sinks:
        G.add_edge(sink, super_sink, capacity=float('inf'))

    # Використовуємо алгоритм Едмондса-Карпа для знаходження максимального потоку
    flow_value, flow_dict = nx.maximum_flow(G, super_source, super_sink, flow_func=nx.algorithms.flow.edmonds_karp)

    # Видаляємо уявне джерело та стік після обчислення
    G.remove_node(super_source)
    G.remove_node(super_sink)

    return flow_value, flow_dict


def calculate_terminal_to_store_flows(flow_dict, sources, intermediate_nodes, sinks):
    terminal_to_store_flows = {}
    for source in sources:
        for sink in sinks:
            total_flow = 0
            for intermediate in intermediate_nodes:
                flow_to_intermediate = flow_dict.get(source, {}).get(intermediate, 0)
                flow_from_intermediate = flow_dict.get(intermediate, {}).get(sink, 0)
                total_flow += min(flow_to_intermediate, flow_from_intermediate)
            terminal_to_store_flows[(source, sink)] = total_flow
    return terminal_to_store_flows


def print_flow_table(terminal_to_store_flows):
    print("| Термінал   | Магазин    | Фактичний Потік (одиниць) |")
    print("| ---------- | ---------- | ------------------------- |")
    for (source, sink), flow in terminal_to_store_flows.items():
        print(f"| {source:<10} | {sink:<10} | {flow:<25} |")


def plot_graph(G):
    # Малюємо граф
    pos = nx.spring_layout(G, seed=42)  # Розташування вузлів
    labels = nx.get_edge_attributes(G, 'capacity')  # Отримуємо пропускні здатності для ребер

    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=3000, font_size=10, font_weight="bold", arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
    plt.title("Граф із пропускними здатностями")
    plt.show()


def main():
    # Побудова графа
    G = build_graph()

    # Визначаємо множину джерел (всі термінали), проміжних вузлів (склади) та множину стоків (всі магазини)
    sources = ["Термінал 1", "Термінал 2"]
    intermediate_nodes = ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]
    sinks = [
        "Магазин 1", "Магазин 2", "Магазин 3", "Магазин 4", "Магазин 5", "Магазин 6",
        "Магазин 7", "Магазин 8", "Магазин 9", "Магазин 10", "Магазин 11", "Магазин 12",
        "Магазин 13", "Магазин 14"
    ]

    # Обчислення максимального потоку
    max_flow, flow_distribution = compute_max_flow(G, sources, sinks)

    print(f"Максимальний потік через всю мережу: {max_flow}")
    print("Розподіл потоку по ребрах:")
    for u, flows in flow_distribution.items():
        for v, flow in flows.items():
            if flow > 0:
                print(f"  {u} -> {v}: {flow}")

    # Обчислення фактичних потоків між терміналами та магазинами
    terminal_to_store_flows = calculate_terminal_to_store_flows(flow_distribution, sources, intermediate_nodes, sinks)

    print("\nТаблиця потоків між терміналами та магазинами:")
    print_flow_table(terminal_to_store_flows)

    # Візуалізація графа
    plot_graph(G)


if __name__ == "__main__":
    main()
