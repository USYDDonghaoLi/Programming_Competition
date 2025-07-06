class Solution:
    def minMoves(self, sx: int, sy: int, tx: int, ty: int) -> int:

        step = 0
        eq = False
        for i in range(60):
            if tx == ty:
                eq = True
            if sx == tx and sy == ty:
                return step
            elif eq and sx == ty and sy == tx:
                return step
            else:
                if tx >= ty:
                    if tx >= 2 * ty:
                        if tx & 1:
                            return -1
                        else:
                            tx >>= 1
                    else:
                        tx -= ty
                else:
                    if ty >= 2 * tx:
                        if ty & 1:
                            return -1
                        else: ty >>= 1
                    else:
                        ty -= tx

                step += 1
            # print('tx, ty', tx, ty)

        return -1