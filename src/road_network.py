import geopandas as gpd
import pandas as pd
import osmnx as ox
import networkx as nx


def load_osm_graph(county_names, network_type="drive"):
    """
    Download and merge OSM graphs for a list of counties.
    """
    graphs = []

    for place in county_names:
        G = ox.graph_from_place(
            place,
            network_type=network_type,
            simplify=True,
            retain_all=True
        )
        graphs.append(G)

    return nx.compose_all(graphs)


def compute_network_features(
    tracts_gdf: gpd.GeoDataFrame,
    county_names,
    projected_crs: str = "EPSG:5070"
):
    """
    Computes:
        - node_density
        - intersection_density
        - street_density

    Returns tract-level GeoDataFrame with added features.
    """

    # Load + convert OSM graph
    G = load_osm_graph(county_names)

    nodes, edges = ox.graph_to_gdfs(G)

    tracts = tracts_gdf.to_crs(projected_crs)
    nodes = nodes.to_crs(projected_crs)
    edges = edges.to_crs(projected_crs)

    if "land_area_km2" not in tracts.columns:
        tracts["land_area_km2"] = tracts.geometry.area / 1e6

    area = tracts.set_index("tract_id")["land_area_km2"]

    # Node density
    nodes_in_tracts = gpd.sjoin(
        nodes,
        tracts[["tract_id", "geometry"]],
        predicate="within"
    )

    node_density = (
        nodes_in_tracts.groupby("tract_id").size()
        / area
    ).rename("node_density")

    # Intersection density
    G_undirected = ox.convert.to_undirected(G)
    degree = dict(G_undirected.degree())

    nodes["degree"] = nodes.index.map(degree).fillna(0)

    intersections = nodes[nodes["degree"] >= 3]

    intersections_in_tracts = gpd.sjoin(
        intersections,
        tracts[["tract_id", "geometry"]],
        predicate="within"
    )

    intersection_density = (
        intersections_in_tracts.groupby("tract_id").size()
        / area
    ).rename("intersection_density")

    # Street density
    edges_with_tracts = gpd.overlay(
        edges,
        tracts[["tract_id", "geometry"]],
        how="intersection"
    )

    edges_with_tracts["length_km"] = edges_with_tracts.geometry.length / 1000

    street_density = (
        edges_with_tracts.groupby("tract_id")["length_km"].sum()
        / area
    ).rename("street_density")

    # Merge output
    features = pd.concat(
        [node_density, intersection_density, street_density],
        axis=1
    ).reset_index()

    return tracts.merge(features, on="tract_id", how="left")