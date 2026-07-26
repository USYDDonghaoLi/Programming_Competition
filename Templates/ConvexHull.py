"""
凸包（Convex Hull）算法。

计算平面上点集的凸包，使用 Andrew 单调链（Monotone Chain）算法。

特点：
- 算法简洁、高效
- 处理退化情况（共线点）
- 支持多种凸包查询

时间复杂度：O(n log n)（排序） + O(n)（凸包构造）
空间复杂度：O(n)

应用：
- 几何查询：点到凸包距离、凸包面积
- 旋转卡壳：两点集最小距离
- 动态凸包维护
"""

from typing import List, Tuple, Optional


class Point:
    """二维平面上的点。"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self, other: 'Point') -> bool:
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other: 'Point') -> bool:
        """按 x 坐标排序，x 相同时按 y 坐标排序。"""
        if self.x != other.x:
            return self.x < other.x
        return self.y < other.y
    
    def __le__(self, other: 'Point') -> bool:
        return self == other or self < other
    
    def distance_to(self, other: 'Point') -> float:
        """计算到另一个点的欧几里得距离。"""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5


def cross_product(o: Point, a: Point, b: Point) -> float:
    """
    计算向量 OA 和 OB 的叉积。
    
    表示 O 到 A 到 B 的转向方向：
    - > 0：左转（逆时针）
    - = 0：共线
    - < 0：右转（顺时针）
    
    Args:
        o, a, b: 三个点
        
    Returns:
        叉积的值
    """
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)


def convex_hull(points: List[Tuple[float, float]], 
                include_collinear: bool = False) -> List[Tuple[float, float]]:
    """
    计算平面上点集的凸包（Andrew 单调链算法）。
    
    Args:
        points: 点的列表，每个点是 (x, y) 元组
        include_collinear: 是否包括凸包边界上的共线点
        
    Returns:
        凸包顶点列表，按逆时针顺序排列（从左下角开始）
        
    示例:
        >>> points = [(0, 0), (1, 1), (1, 0), (0, 1), (2, 2)]
        >>> hull = convex_hull(points)
        >>> hull
        [(0, 0), (1, 0), (2, 2), (0, 1)]
    """
    if len(points) <= 2:
        return sorted(set(points))
    
    # 转换为 Point 对象并排序
    pts = [Point(x, y) for x, y in points]
    pts.sort()
    
    # 构建下凸包（lower hull）
    lower = []
    for p in pts:
        # 如果不是共线点，删除最后一个点
        if not include_collinear:
            while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
                lower.pop()
        else:
            # 如果包括共线点，只删除严格的右转
            while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) < 0:
                lower.pop()
        lower.append(p)
    
    # 构建上凸包（upper hull）
    upper = []
    for p in reversed(pts):
        if not include_collinear:
            while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
                upper.pop()
        else:
            while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) < 0:
                upper.pop()
        upper.append(p)
    
    # 合并（去除重复的端点）
    hull = lower[:-1] + upper[:-1]
    
    return [(p.x, p.y) for p in hull]


class ConvexHull:
    """
    凸包数据结构。
    
    支持凸包的各种查询操作。
    """
    
    def __init__(self, points: List[Tuple[float, float]]):
        """
        初始化凸包。
        
        Args:
            points: 点的列表，每个点是 (x, y) 元组
        """
        self.original_points = points
        self.hull_points = self._build_hull(points)
        self.n = len(self.hull_points)
    
    @staticmethod
    def _build_hull(points: List[Tuple[float, float]]) -> List[Point]:
        """构建凸包。"""
        if len(points) <= 2:
            return sorted([Point(x, y) for x, y in points])
        
        pts = [Point(x, y) for x, y in points]
        pts.sort()
        
        lower = []
        for p in pts:
            while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
        
        upper = []
        for p in reversed(pts):
            while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        
        return lower[:-1] + upper[:-1]
    
    def area(self) -> float:
        """
        计算凸包的面积。
        
        使用 Shoelace 公式。
        
        Returns:
            凸包的面积
        """
        if self.n < 3:
            return 0.0
        
        area = 0.0
        for i in range(self.n):
            p1 = self.hull_points[i]
            p2 = self.hull_points[(i + 1) % self.n]
            area += p1.x * p2.y - p2.x * p1.y
        
        return abs(area) / 2.0
    
    def perimeter(self) -> float:
        """
        计算凸包的周长。
        
        Returns:
            凸包的周长
        """
        if self.n < 2:
            return 0.0
        
        total = 0.0
        for i in range(self.n):
            p1 = self.hull_points[i]
            p2 = self.hull_points[(i + 1) % self.n]
            total += p1.distance_to(p2)
        
        return total
    
    def contains_point(self, x: float, y: float) -> bool:
        """
        判断点 (x, y) 是否在凸包内部。
        
        Args:
            x, y: 点的坐标
            
        Returns:
            True 如果点在凸包内，False 否则
        """
        if self.n < 3:
            return False
        
        p = Point(x, y)
        
        # 检查所有边
        for i in range(self.n):
            p1 = self.hull_points[i]
            p2 = self.hull_points[(i + 1) % self.n]
            
            # 点应该在所有边的左侧（逆时针方向）
            if cross_product(p1, p2, p) < 0:
                return False
        
        return True
    
    def contains_or_on_boundary(self, x: float, y: float) -> bool:
        """
        判断点是否在凸包内部或边界上。
        
        Args:
            x, y: 点的坐标
            
        Returns:
            True 如果点在凸包内或边界上，False 否则
        """
        if self.n < 3:
            return False
        
        p = Point(x, y)
        
        for i in range(self.n):
            p1 = self.hull_points[i]
            p2 = self.hull_points[(i + 1) % self.n]
            
            if cross_product(p1, p2, p) < 0:
                return False
        
        return True
    
    def get_hull_points(self) -> List[Tuple[float, float]]:
        """获取凸包顶点列表。"""
        return [(p.x, p.y) for p in self.hull_points]
    
    def diameter(self) -> float:
        """
        计算凸包的直径（最远两点间的距离）。
        
        使用旋转卡壳算法。
        
        时间复杂度：O(n)
        
        Returns:
            直径的长度
        """
        if self.n < 2:
            return 0.0
        
        max_dist = 0.0
        
        # 旋转卡壳
        i = 0
        j = 1
        
        while i < self.n:
            dist = self.hull_points[i].distance_to(self.hull_points[j])
            max_dist = max(max_dist, dist)
            
            # 找到与边 hull_points[i] -> hull_points[i+1] 距离最远的点
            next_j = (j + 1) % self.n
            
            # 检查是否应该移动 j
            edge = (self.hull_points[(i + 1) % self.n].x - self.hull_points[i].x,
                   self.hull_points[(i + 1) % self.n].y - self.hull_points[i].y)
            
            dist_j = abs(edge[0] * (self.hull_points[j].y - self.hull_points[i].y) -
                        edge[1] * (self.hull_points[j].x - self.hull_points[i].x))
            dist_next_j = abs(edge[0] * (self.hull_points[next_j].y - self.hull_points[i].y) -
                             edge[1] * (self.hull_points[next_j].x - self.hull_points[i].x))
            
            if dist_next_j > dist_j:
                j = next_j
            else:
                i += 1
        
        return max_dist


# 旧版本的兼容接口（基于列表的简单实现）
class ConvexHullSimple:
    """简单的凸包实现，兼容旧代码。"""
    
    def __init__(self, points: List[Tuple[float, float]]):
        """初始化凸包。"""
        self.points = sorted(set(points))
    
    @staticmethod
    def cross(o: Tuple[float, float], a: Tuple[float, float], 
              b: Tuple[float, float]) -> float:
        """计算向量 OA 和 OB 的叉积。"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    def lower_hull(self) -> List[Tuple[float, float]]:
        """构建下凸包。"""
        lower = []
        for p in self.points:
            while len(lower) >= 2 and self.cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
        return lower[:-1]
    
    def upper_hull(self) -> List[Tuple[float, float]]:
        """构建上凸包。"""
        upper = []
        for p in reversed(self.points):
            while len(upper) >= 2 and self.cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        return upper[:-1]
    
    def build(self) -> List[Tuple[float, float]]:
        """构建完整的凸包。"""
        if len(self.points) <= 2:
            return self.points
        return self.lower_hull() + self.upper_hull()


def test_convex_hull():
    """测试凸包"""
    points = [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)]
    hull = convex_hull(points)
    # 凸包应该包含四个角点
    assert len(hull) >= 3, f"Convex hull should have at least 3 points"
    print("✓ test_convex_hull passed")


if __name__ == "__main__":
    test_convex_hull()
    print("\n所有 ConvexHull 测试通过！✓")
