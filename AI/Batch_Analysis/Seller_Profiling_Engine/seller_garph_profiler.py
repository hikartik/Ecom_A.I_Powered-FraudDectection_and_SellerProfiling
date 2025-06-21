import torch
import torch.nn.functional as F
from torch_geometric.nn import HeteroConv, GATConv, Linear
from torch_geometric.data import HeteroData

class SellerGraphModel(torch.nn.Module):
    def __init__(self, hidden_channels=32):
        super().__init__()
        self.conv1 = HeteroConv({
            ('vision', 'to', 'product'): GATConv(-1, hidden_channels, add_self_loops=False),
            ('text', 'to', 'product'): GATConv(-1, hidden_channels, add_self_loops=False),
            ('multimodal', 'to', 'product'): GATConv(-1, hidden_channels, add_self_loops=False),
            ('ensemble', 'to', 'product'): GATConv(-1, hidden_channels, add_self_loops=False),
            ('review', 'to', 'product'): GATConv(-1, hidden_channels, add_self_loops=False),
            ('product', 'to', 'seller'): GATConv(-1, hidden_channels, add_self_loops=False),
        }, aggr='sum')

        self.seller_out = Linear(hidden_channels, 1)

    def forward(self, seller_input):
        data = build_seller_graph(seller_input)
        x_dict, edge_index_dict = data.x_dict, data.edge_index_dict
        x_dict = self.conv1(x_dict, edge_index_dict)
        seller_emb = x_dict['seller']
        return torch.sigmoid(self.seller_out(seller_emb)).squeeze()

def build_seller_graph(seller_input: dict) -> HeteroData:
    """
    seller_input: dict with keys:
    - seller_features: Tensor [1, F]
    - product_features: List of dicts with keys:
        - vision: [1, F]
        - text: [1, F]
        - multimodal: [1, F]
        - ensemble: [1, F]
        - reviews: List of [1, F] tensors
    """
    data = HeteroData()

    # Seller node
    data['seller'].x = seller_input['seller_features']  # [1, F]

    vision_nodes, text_nodes, multi_nodes, ens_nodes, review_nodes = [], [], [], [], []
    product_nodes = []

    edge_vision_product = []
    edge_text_product = []
    edge_multimodal_product = []
    edge_ensemble_product = []
    edge_review_product = []
    edge_product_seller = []

    for i, p in enumerate(seller_input['product_features']):
        product_nodes.append(torch.zeros(1, 1))

        # Add score nodes
        vision_nodes.append(p['vision'])
        text_nodes.append(p['text'])
        multi_nodes.append(p['multimodal'])
        ens_nodes.append(p['ensemble'])

        # Add review nodes
        review_start_idx = len(review_nodes)
        review_nodes.extend(p['reviews'])

        # Edges from scores to product node
        edge_vision_product.append([len(vision_nodes) - 1, i])
        edge_text_product.append([len(text_nodes) - 1, i])
        edge_multimodal_product.append([len(multi_nodes) - 1, i])
        edge_ensemble_product.append([len(ens_nodes) - 1, i])

        for j in range(len(p['reviews'])):
            edge_review_product.append([review_start_idx + j, i])

        edge_product_seller.append([i, 0])  # product to seller

    # Stack nodes
    data['vision'].x = torch.cat(vision_nodes, dim=0)
    data['text'].x = torch.cat(text_nodes, dim=0)
    data['multimodal'].x = torch.cat(multi_nodes, dim=0)
    data['ensemble'].x = torch.cat(ens_nodes, dim=0)
    data['review'].x = torch.cat(review_nodes, dim=0) if review_nodes else torch.empty((0, vision_nodes[0].shape[1]))
    data['product'].x = torch.cat(product_nodes, dim=0)

    # Edges
    def to_edge_index(edge_list):
        if not edge_list:
            return torch.empty((2, 0), dtype=torch.long)
        return torch.tensor(edge_list, dtype=torch.long).t().contiguous()

    data['vision', 'to', 'product'].edge_index = to_edge_index(edge_vision_product)
    data['text', 'to', 'product'].edge_index = to_edge_index(edge_text_product)
    data['multimodal', 'to', 'product'].edge_index = to_edge_index(edge_multimodal_product)
    data['ensemble', 'to', 'product'].edge_index = to_edge_index(edge_ensemble_product)
    data['review', 'to', 'product'].edge_index = to_edge_index(edge_review_product)
    data['product', 'to', 'seller'].edge_index = to_edge_index(edge_product_seller)

    return data
