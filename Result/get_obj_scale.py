import trimesh

# ????OBJ???
mesh = trimesh.load(r'C:\Users\124512\xwechat_files\wxid_btn8ohukaloa12_cc7f\msg\file\2025-09\Deploy_2025-07-24-18-47-26\Deploy_2025-07-24-18-47-26\deploy\algs_bs\boundary_walls.obj')


# 遍历所有边并计算长度
edges = mesh.edges_unique  # 唯一边（去重）
vertices = mesh.vertices
edge_lengths = []

for edge in edges:
    v1, v2 = vertices[edge[0]], vertices[edge[1]]
    length = trimesh.util.euclidean(v1, v2)  # 计算欧氏距离
    edge_lengths.append(length)

# 打印结果
print(f"总边数: {len(edges)}")
print(f"边长示例: {edge_lengths[:9]}")  # 输出前5条边的长度