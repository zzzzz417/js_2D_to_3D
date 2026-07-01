def ply_to_js_scale(ply_path, k=1.0):
    vertices_raw = []
    faces = []
    vert_count = 0
    face_count = 0
    in_header = True
    v_read = 0
    f_read = 0

    with open(ply_path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            # 解析头部字段
            if in_header:
                if s.startswith("element vertex"):
                    vert_count = int(s.split()[-1])
                elif s.startswith("element face"):
                    face_count = int(s.split()[-1])
                elif s == "end_header":
                    in_header = False
                continue
            # 读取顶点XYZ
            if v_read < vert_count:
                x, y, z = map(float, s.split()[:3])
                vertices_raw.append([x, y, z])
                v_read += 1
            # 读取三角面片索引（仅取前3个顶点，适配三角网格）
            elif f_read < face_count:
                nums = list(map(int, s.split()))
                tri = nums[1:4]
                faces.append(f'[{tri[0]},{tri[1]},{tri[2]}]')
                f_read += 1

    # 三轴全部归一到 [-k, k]
    xs = [p[0] for p in vertices_raw]
    ys = [p[1] for p in vertices_raw]
    zs = [p[2] for p in vertices_raw]
    
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    z_min, z_max = min(zs), max(zs)

    vertices_out = []
    for x, y, z in vertices_raw:
        x_scaled = 2 * k * (x - x_min) / (x_max - x_min) - k
        y_scaled = 2 * k * (y - y_min) / (y_max - y_min) - k
        z_scaled = 2 * k * (z - z_min) / (z_max - z_min) - k
        y_scaled *= 1
        vertices_out.append(f'{{x:{x_scaled:.6f}, y:{y_scaled:.6f}, z:{z_scaled:.6f}}}')

    # ES Module 导出语句，前端import直接使用
    vs_str = "export const vs = [\n    " + ",\n    ".join(vertices_out) + "\n]"
    fs_str = "export const fs = [\n    " + ",\n    ".join(faces) + "\n]"
    full_code = vs_str + "\n\n" + fs_str
    return full_code

if __name__ == "__main__":
    try:
        # 可自定义k，范围 [-k, k]
        k_value = 5.0
        output = ply_to_js_scale("tux.ply", k=k_value)
        # 直接生成前端专用 data.js，替换txt
        with open("data.js", "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 转换成功！X/Y/Z全部映射至 [-{k_value}, {k_value}]")
        print(f"📄 模型数据已写入 data.js，可直接在main.js import")
    except FileNotFoundError:
        print("❌ 错误：当前目录未找到 tux.ply 文件，请确认文件路径")
    except Exception as err:
        print(f"❌ 转换失败：{str(err)}")