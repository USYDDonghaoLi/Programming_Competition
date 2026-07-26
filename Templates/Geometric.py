"""
计算几何库：完整的二维平面几何算法库。

包含：
1. 点 (Point)：基本的 2D 向量和点操作
2. 直线 (Line)：直线表示和查询
3. 线段 (Segment)：线段表示和相交测试
4. 多边形 (Polygon)：多边形面积、凸性检查、点包含测试
5. 圆 (Circle)：圆的各种查询和相交测试
6. 辅助函数：凸包、极角排序等

精度控制：eps = 1e-9（浮点数比较误差范围）

时间复杂度概览：
- 点、向量操作：O(1)
- 直线相交、点投影：O(1)
- 线段相交：O(1)
- 多边形面积、点包含：O(n)
- 圆-圆/直线/线段相交：O(1)
- 凸包：O(n log n)
"""

import math
from typing import List, Optional, Tuple, Union


# 全局精度参数
EPS = 1e-9


def is_zero(x: float, eps: float = EPS) -> bool:
    """判断浮点数是否为零。"""
    return abs(x) <= eps


def equal(a: float, b: float, eps: float = EPS) -> bool:
    """判断两个浮点数是否相等。"""
    return abs(a - b) <= eps


class Point:
    """
    二维平面上的点/向量。
    
    既可表示几何点，也可表示向量。
    支持向量加法、减法、数乘、点积、叉积等操作。
    
    属性：
    - x, y: 坐标
    """
    
    def __init__(self, x: float, y: float):
        """初始化点。"""
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"Point({self.x:.6f}, {self.y:.6f})"
    
    def __eq__(self, other: 'Point') -> bool:
        """判断两点是否相等（在精度范围内）。"""
        return equal(self.x, other.x) and equal(self.y, other.y)
    
    def __add__(self, other: 'Point') -> 'Point':
        """向量加法。"""
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point') -> 'Point':
        """向量减法。"""
        return Point(self.x - other.x, self.y - other.y)
    
    def __neg__(self) -> 'Point':
        """向量取反。"""
        return Point(-self.x, -self.y)
    
    def __mul__(self, other: Union['Point', float]) -> Union['Point', float]:
        """
        支持两种乘法：
        - 点积：Point * Point → float
        - 数乘：Point * float → Point
        """
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y  # 点积
        return Point(self.x * other, self.y * other)    # 数乘
    
    def __rmul__(self, k: float) -> 'Point':
        """支持 k * Point。"""
        return Point(self.x * k, self.y * k)
    
    def __truediv__(self, k: float) -> 'Point':
        """向量除以标量。"""
        return Point(self.x / k, self.y / k)
    
    def __xor__(self, other: 'Point') -> float:
        """叉积（使用 ^ 操作符）。返回 self × other。"""
        return self.x * other.y - self.y * other.x
    
    def dot(self, other: 'Point') -> float:
        """显式点积：self · other。"""
        return self.x * other.x + self.y * other.y
    
    def cross(self, other: 'Point') -> float:
        """显式叉积：self × other。"""
        return self.x * other.y - self.y * other.x
    
    def toleft(self, other: 'Point') -> int:
        """
        判断当前向量相对于 other 的转向。
        
        计算 self × other 的符号：
        - 返回  1：左转（逆时针，cross > 0）
        - 返回 -1：右转（顺时针，cross < 0）
        - 返回  0：共线
        """
        t = self.cross(other)
        return (t > EPS) - (t < -EPS)
    
    def len2(self) -> float:
        """向量长度的平方（用于避免开方）。"""
        return self.x * self.x + self.y * self.y
    
    def len(self) -> float:
        """向量长度。"""
        return math.sqrt(self.len2())
    
    def dis2(self, other: 'Point') -> float:
        """到另一点的距离的平方。"""
        return (other - self).len2()
    
    def dis(self, other: 'Point') -> float:
        """到另一点的距离（欧几里得距离）。"""
        return math.sqrt(self.dis2(other))
    
    def rotate(self, alpha: float) -> 'Point':
        """
        逆时针旋转 alpha 弧度。
        
        使用旋转矩阵：
        [cos(α)  -sin(α)] [x]
        [sin(α)   cos(α)] [y]
        
        Args:
            alpha: 旋转角度（弧度，正数为逆时针）
            
        Returns:
            旋转后的点
        """
        cos_a = math.cos(alpha)
        sin_a = math.sin(alpha)
        return Point(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
    
    def normalize(self) -> 'Point':
        """
        返回单位向量（方向相同，长度为 1）。
        
        如果长度为 0，返回零向量。
        """
        length = self.len()
        return self / length if length > EPS else Point(0, 0)
    
    def perpendicular(self) -> 'Point':
        """
        返回垂直向量（逆时针旋转 90 度）。
        
        如果原向量是 (x, y)，垂直向量是 (-y, x)。
        """
        return Point(-self.y, self.x)
    
    def angle(self) -> float:
        """
        返回向量的极角（与 x 轴正方向的夹角）。
        
        范围：[-π, π]
        """
        return math.atan2(self.y, self.x)


class Line:
    """
    直线的参数方程表示。
    
    直线上的点表示为：p + t * v，其中：
    - p：直线上一点（基点）
    - v：方向向量
    
    属性：
    - p: 基点
    - v: 方向向量
    """
    
    def __init__(self, p: Point, v: Point):
        """
        初始化直线。
        
        Args:
            p: 直线上的一点
            v: 方向向量（不需要标准化）
        """
        self.p = p
        self.v = v
    
    def toleft(self, a: Point) -> int:
        """
        判断点 a 在直线的左侧、右侧还是直线上。
        
        Returns:
            1：左侧，-1：右侧，0：在直线上
        """
        return self.v.toleft(a - self.p)
    
    def inter(self, l: 'Line') -> Optional[Point]:
        """
        求两条直线的交点。
        
        Args:
            l: 另一条直线
            
        Returns:
            交点；如果平行则返回 None
        """
        d = self.v.cross(l.v)
        if is_zero(d):
            return None
        u = self.p - l.p
        t = l.v.cross(u) / d
        return self.p + self.v * t
    
    def projection(self, a: Point) -> Point:
        """
        求点 a 在直线上的投影。
        
        Args:
            a: 点
            
        Returns:
            a 在直线上的投影点
        """
        t = ((a - self.p) * self.v) / (self.v * self.v)
        return self.p + self.v * t
    
    def dis(self, a: Point) -> float:
        """
        求点到直线的距离。
        
        使用公式：d = |向量叉积| / |方向向量长度|
        
        Args:
            a: 点
            
        Returns:
            点 a 到直线的距离
        """
        return abs((self.p - a).cross(self.v)) / self.v.len()



class Segment:
    """
    线段表示。
    
    线段由两个端点确定。
    
    属性：
    - a, b: 两个端点
    """
    
    def __init__(self, a: Point, b: Point):
        """初始化线段。"""
        self.a = a
        self.b = b
    
    def is_on(self, p: Point) -> bool:
        """
        判断点 p 是否在线段上。
        
        需要满足两个条件：
        1. p 在直线 ab 上（叉积为 0）
        2. p 在线段范围内（投影点积为负）
        
        Args:
            p: 点
            
        Returns:
            True 如果 p 在线段上，包括端点
        """
        if self.a == p or self.b == p:
            return True
        # 叉积为 0 且点积为负表示点在线段内
        return (is_zero((p - self.a).cross(p - self.b)) and 
                (p - self.a) * (p - self.b) < 0)
    
    def is_inter_line(self, l: Line) -> bool:
        """
        判断线段是否与直线相交。
        
        Args:
            l: 直线
            
        Returns:
            True 如果线段与直线有交点
        """
        # 端点在直线上或两端点在直线两侧
        return (is_zero(l.toleft(self.a)) or is_zero(l.toleft(self.b)) or
                l.toleft(self.a) * l.toleft(self.b) == -1)
    
    def is_inter_segment(self, s: 'Segment') -> bool:
        """
        判断两线段是否相交（包括接触）。
        
        两线段相交当且仅当：
        1. 存在端点在对方线段上，或
        2. 两线段的端点分别在对方直线的两侧
        
        Args:
            s: 另一线段
            
        Returns:
            True 如果两线段相交或接触
        """
        # 检查端点是否在对方线段上
        if (self.is_on(s.a) or self.is_on(s.b) or 
            s.is_on(self.a) or s.is_on(self.b)):
            return True
        
        # 检查线段端点是否在对方直线两侧
        l1 = Line(self.a, self.b - self.a)
        l2 = Line(s.a, s.b - s.a)
        return (l1.toleft(s.a) * l1.toleft(s.b) == -1 and
                l2.toleft(self.a) * l2.toleft(self.b) == -1)
    
    def dis_point(self, p: Point) -> float:
        """
        点到线段的距离。
        
        如果点的投影在线段外，返回点到最近端点的距离；
        否则返回点到线段所在直线的距离。
        
        Args:
            p: 点
            
        Returns:
            点 p 到线段的距离
        """
        # 检查投影是否在线段范围外
        if ((p - self.a) * (self.b - self.a) < -EPS or 
            (p - self.b) * (self.a - self.b) < -EPS):
            return min(p.dis(self.a), p.dis(self.b))
        
        # 投影在线段范围内，返回点到直线的距离
        l = Line(self.a, self.b - self.a)
        return l.dis(p)
    
    def dis_segment(self, s: 'Segment') -> float:
        """
        两线段之间的距离。
        
        如果相交则距离为 0；
        否则为最小端点对距离。
        
        Args:
            s: 另一线段
            
        Returns:
            两线段的距离
        """
        if self.is_inter_segment(s):
            return 0
        return min(self.dis_point(s.a), self.dis_point(s.b),
                   s.dis_point(self.a), s.dis_point(self.b))



class Polygon:
    """
    多边形表示。
    
    由有序的点列表表示，点按逆时针（CCW）或顺时针（CW）顺序排列。
    
    属性：
    - points: 多边形顶点列表
    """
    
    def __init__(self, points: List[Point] = None):
        """初始化多边形。"""
        self.points = points or []
    
    def nxt(self, i: int) -> int:
        """获取下一个顶点的索引（循环）。"""
        return 0 if i == len(self.points) - 1 else i + 1
    
    def pre(self, i: int) -> int:
        """获取前一个顶点的索引（循环）。"""
        return len(self.points) - 1 if i == 0 else i - 1
    
    def area(self) -> float:
        """
        计算多边形面积。
        
        使用 Shoelace 公式（鞋带公式）：
        面积 = 1/2 * |Σ(cross(p_i, p_{i+1}))|
        
        Returns:
            多边形的有向面积（逆时针为正，顺时针为负）
        """
        res = 0.0
        for i in range(len(self.points)):
            res += self.points[i].cross(self.points[self.nxt(i)])
        return res / 2.0
    
    def is_convex(self) -> bool:
        """
        判断多边形是否为凸多边形。
        
        凸多边形的所有顶点的叉积都应该是同号的。
        
        Returns:
            True 如果是凸多边形
        """
        n = len(self.points)
        if n < 3:
            return True
        
        for i in range(n):
            # 相邻三个点的叉积
            cross_prod = ((self.points[self.nxt(i)] - self.points[i]) * 
                         (self.points[self.pre(i)] - self.points[i]))
            if cross_prod < -EPS:
                return False
        return True
    
    def is_in(self, a: Point) -> int:
        """
        判断点是否在多边形内。
        
        使用 Ray Casting 算法（射线法）：
        从点向任意方向发射射线，统计与多边形边的交点数。
        
        Args:
            a: 待测试的点
            
        Returns:
            0：严格在多边形外
            1：在多边形边界上
            2：严格在多边形内部
        """
        if not self.points:
            return 0
        
        # 先检查是否在边界上
        for i in range(len(self.points)):
            s = Segment(self.points[i], self.points[self.nxt(i)])
            if s.is_on(a):
                return 1
        
        # 使用水平射线法
        count = 0
        for i in range(len(self.points)):
            p1 = self.points[i] - a
            p2 = self.points[self.nxt(i)] - a
            
            # 确保 p1.y <= p2.y
            if p1.y > p2.y:
                p1, p2 = p2, p1
            
            # 射线向右，检查边是否跨越水平线
            if p1.y < EPS < p2.y and p1.cross(p2) > EPS:
                count ^= 1
        
        return 2 if count else 0
    
    def winding_number(self, a: Point) -> int:
        """
        计算点的缠绕数（Winding Number）。
        
        对于有向多边形，缠绕数表示点被多边形边界"环绕"的次数和方向。
        
        Args:
            a: 待测试的点
            
        Returns:
            缠绕数（0 表示在外部，非 0 表示在内部）
        """
        winding = 0
        for i in range(len(self.points)):
            s = Segment(self.points[i], self.points[self.nxt(i)])
            if s.is_on(a):
                return -10000  # 标记为在边界上
            
            p1 = self.points[i] - a
            p2 = self.points[self.nxt(i)] - a
            
            flag = False
            if p1.y > p2.y:
                p1, p2 = p2, p1
                flag = True
            
            if p1.y < EPS < p2.y and p1.cross(p2) > EPS:
                winding += -1 if flag else 1
        
        return winding



# ===================== 常用辅助函数 =====================

def convex_hull(points: List[Point]) -> 'Polygon':
    """
    使用 Andrew 单调栈算法求凸包。
    
    算法流程：
    1. 按 x 坐标排序（相同 x 按 y 坐标排序）
    2. 扫描得到下凸壳
    3. 逆序扫描得到上凸壳
    4. 合并两个凸壳
    
    时间复杂度：O(n log n)
    
    Args:
        points: 点的列表
        
    Returns:
        凸包（多边形）
    """
    if len(points) <= 1:
        return Polygon(points[:])
    
    # 按字典序排序
    points = sorted(points, key=lambda p: (p.x, p.y))
    
    # 构建下凸壳
    lower = []
    for p in points:
        while len(lower) >= 2 and (lower[-1] - lower[-2]).cross(p - lower[-2]) <= 0:
            lower.pop()
        lower.append(p)
    
    # 构建上凸壳
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and (upper[-1] - upper[-2]).cross(p - upper[-2]) <= 0:
            upper.pop()
        upper.append(p)
    
    # 合并（去掉重复的端点）
    hull = lower[:-1] + upper[:-1]
    return Polygon(hull)


def polar_sort(points: List[Point], origin: Point = None) -> List[Point]:
    """
    按极角排序。
    
    以 origin 为极点，将所有点按极角排序。
    如果不指定原点，默认为最左下的点。
    
    Args:
        points: 点的列表
        origin: 极点（默认为最左下点）
        
    Returns:
        按极角排序后的点列表
    """
    if origin is None:
        origin = min(points, key=lambda p: (p.y, p.x))
    
    def key_func(p: Point) -> Tuple[float, float]:
        """按极角排序，相同极角按距离排序。"""
        return ((p - origin).angle(), (p - origin).len2())
    
    return sorted(points, key=key_func)


class Circle:
    """
    圆的表示与查询。
    
    属性：
    - c: 圆心
    - r: 半径
    """
    
    def __init__(self, center: Point, radius: float):
        """初始化圆。"""
        self.c = center
        self.r = radius
    
    def area(self) -> float:
        """圆的面积。"""
        return math.pi * self.r * self.r
    
    def contain_point(self, p: Point) -> int:
        """
        判断点与圆的位置关系。
        
        Args:
            p: 点
            
        Returns:
            0：在圆外，1：在圆周上，2：在圆内
        """
        d = p.dis(self.c)
        if equal(d, self.r):
            return 1
        return 2 if d < self.r - EPS else 0
    
    # =================== 两圆相关 ===================
    
    def relation(self, other: 'Circle') -> int:
        """
        判断两圆的相对位置。
        
        Args:
            other: 另一个圆
            
        Returns:
            0：外离
            1：外切
            2：相交
            3：内切
            4：内含
        """
        d = self.c.dis(other.c)
        r1, r2 = self.r, other.r
        
        if d > r1 + r2 + EPS:
            return 0  # 外离
        if equal(d, r1 + r2):
            return 1  # 外切
        if equal(d, abs(r1 - r2)):
            return 3  # 内切
        if d < abs(r1 - r2) - EPS:
            return 4  # 内含
        return 2  # 相交
    
    def inter(self, other: 'Circle') -> List[Point]:
        """
        求两圆的交点。
        
        Args:
            other: 另一个圆
            
        Returns:
            交点列表（0、1 或 2 个点）
        """
        rel = self.relation(other)
        
        # 不相交的情况
        if rel == 0 or rel == 4:
            return []
        
        d = self.c.dis(other.c)
        
        # 同心圆
        if d < EPS:
            return []
        
        # 使用三角形法求交点
        # a：self 圆心到交点所在垂线的距离
        a = (self.r * self.r - other.r * other.r + d * d) / (2 * d)
        h_sq = self.r * self.r - a * a
        
        if h_sq < -EPS:
            return []
        
        h = math.sqrt(max(h_sq, 0.0))
        
        # 垂线所在点
        mid = self.c + (other.c - self.c) * (a / d)
        
        # 相切的情况
        if h < EPS:
            return [mid]
        
        # 相交：两个交点
        perp = (other.c - self.c).perpendicular().normalize() * h
        return [mid + perp, mid - perp]
    
    # =================== 直线与圆 ===================
    
    def line_relation(self, l: Line) -> int:
        """
        判断直线与圆的相对位置。
        
        Args:
            l: 直线
            
        Returns:
            0：相离，1：相切，2：相交
        """
        d = l.dis(self.c)
        if d > self.r + EPS:
            return 0  # 相离
        if equal(d, self.r):
            return 1  # 相切
        return 2  # 相交
    
    def line_inter(self, l: Line) -> List[Point]:
        """
        求直线与圆的交点。
        
        Args:
            l: 直线
            
        Returns:
            交点列表（0、1 或 2 个点）
        """
        d = l.dis(self.c)
        
        if d > self.r + EPS:
            return []
        
        # 圆心在直线上的投影
        proj = l.projection(self.c)
        
        # 相切的情况
        if equal(d, self.r):
            return [proj]
        
        # 相交：求两个交点
        h = math.sqrt(max(self.r * self.r - d * d, 0.0))
        dir_unit = l.v.normalize()
        return [proj + dir_unit * h, proj - dir_unit * h]
    
    # =================== 射线与圆 ===================
    
    def ray_inter(self, origin: Point, direction: Point) -> List[Point]:
        """
        求射线与圆的交点。
        
        射线方程：origin + t * direction，其中 t >= 0
        
        Args:
            origin: 射线的起点
            direction: 射线的方向
            
        Returns:
            交点列表，按到 origin 的距离从近到远排序
        """
        line = Line(origin, direction)
        inters = self.line_inter(line)
        
        # 过滤出射线上的交点
        res = []
        for p in inters:
            if (p - origin) * direction >= -EPS:
                res.append(p)
        
        # 按距离排序
        res.sort(key=lambda p: p.dis2(origin))
        return res
    
    # =================== 线段与圆 ===================
    
    def segment_inter(self, s: Segment) -> List[Point]:
        """
        求线段与圆的交点。
        
        只返回在线段上的交点。
        
        Args:
            s: 线段
            
        Returns:
            交点列表（在线段内）
        """
        line = Line(s.a, s.b - s.a)
        inters = self.line_inter(line)
        
        res = []
        for p in inters:
            if s.is_on(p):
                res.append(p)
        
        return res


# ==================== 高级几何函数 ====================

def segment_line_inter(seg: Segment, line: Line) -> Optional[Point]:
    """
    求线段与直线的交点。
    
    Args:
        seg: 线段
        line: 直线
        
    Returns:
        交点；如果不相交或平行则返回 None
    """
    if not seg.is_inter_line(line):
        return None
    
    # 参数方程求交点
    l = Line(seg.a, seg.b - seg.a)
    inter_point = l.inter(line)
    
    if inter_point is None:
        return None
    
    # 检查交点是否在线段上
    if seg.is_on(inter_point):
        return inter_point
    
    return None


def tangent_of_circle(p: Point, circle: Circle) -> List[Line]:
    """
    求从点 p 到圆的切线。
    
    Args:
        p: 外部的点
        circle: 圆
        
    Returns:
        切线列表（通常 0、1 或 2 条）
    """
    d = p.dis(circle.c)
    
    # 点在圆内
    if d < circle.r - EPS:
        return []
    
    # 点在圆周上
    if equal(d, circle.r):
        # 只有一条切线
        v = (p - circle.c).perpendicular()
        return [Line(p, v)]
    
    # 点在圆外，有两条切线
    # 利用勾股定理：切线长 = sqrt(d² - r²)
    tangent_len = math.sqrt(max(d * d - circle.r * circle.r, 0.0))
    
    # 切点方向
    angle = math.asin(circle.r / d)
    
    v1 = (circle.c - p).normalize().rotate(angle)
    v2 = (circle.c - p).normalize().rotate(-angle)
    
    return [Line(p, v1), Line(p, v2)]


def perpendicular_bisector(p1: Point, p2: Point) -> Line:
    """
    求两点的垂直平分线。
    
    Args:
        p1, p2: 两个点
        
    Returns:
        垂直平分线
    """
    mid = (p1 + p2) / 2
    direction = (p2 - p1).perpendicular()
    return Line(mid, direction)


def angle_bisector(p: Point, a: Point, b: Point) -> Line:
    """
    求角的平分线。
    
    从点 p 出发，∠APB 的角平分线。
    
    Args:
        p: 角的顶点
        a, b: 角的两条边上的点
        
    Returns:
        角平分线
    """
    # 两个方向的单位向量
    u1 = (a - p).normalize()
    u2 = (b - p).normalize()
    
    # 平分线方向
    direction = u1 + u2
    
    return Line(p, direction)


def distance_point_to_polygon(p: Point, polygon: Polygon) -> float:
    """
    求点到多边形的距离。
    
    如果点在多边形内，返回 0；否则返回到最近边的距离。
    
    Args:
        p: 点
        polygon: 多边形
        
    Returns:
        点到多边形的距离
    """
    # 如果点在多边形内
    if polygon.is_in(p) >= 1:
        return 0
    
    # 计算到所有边的最小距离
    min_dist = float('inf')
    for i in range(len(polygon.points)):
        seg = Segment(polygon.points[i], 
                     polygon.points[polygon.nxt(i)])
        dist = seg.dis_point(p)
        min_dist = min(min_dist, dist)
    
    return min_dist


def rotate_polygon(polygon: Polygon, origin: Point, angle: float) -> Polygon:
    """
    旋转多边形。
    
    Args:
        polygon: 原多边形
        origin: 旋转中心
        angle: 旋转角度（弧度）
        
    Returns:
        旋转后的多边形
    """
    new_points = []
    for p in polygon.points:
        # 平移到原点，旋转，再平移回去
        rotated = (p - origin).rotate(angle) + origin
        new_points.append(rotated)
    
    return Polygon(new_points)



def test_geometric():
    """测试几何库"""
    # 测试点
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    
    # 距离测试
    dist = p2.dis(p1)
    assert abs(dist - 5) < 1e-9, f"Expected 5, got {dist}"
    print("✓ test_point_distance passed")
    
    # 点的长度
    assert abs(p2.len() - 5) < 1e-9, f"Expected 5, got {p2.len()}"
    print("✓ test_point_length passed")
    
    # 线段长度 = 两点距离
    seg = Segment(p1, p2)
    seg_length = p1.dis(p2)
    assert abs(seg_length - 5) < 1e-9, f"Expected 5, got {seg_length}"
    print("✓ test_segment_length passed")


if __name__ == "__main__":
    test_geometric()
    print("\n所有几何测试通过！✓")
