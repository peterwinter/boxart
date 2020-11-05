import pandas as pd
import random


class BlockColorPicker():

    def __init__(self, colors, blocks=None):

        self.colors = colors
        self.c2 = set(colors)

        # calculated when blocks is passed in.
        self.block_df = None
        self.block_neighbors = None
        self.block_colors = None
        self.colored_blocks = None
        self.patches = None

        if blocks is not None:
            self.load_blocks(blocks)


    def load_blocks(self, blocks):
        self.blocks = blocks
        self.block_df = pd.DataFrame(blocks).set_index('id')
        self.block_neighbors = self._blocks_to_graph(df= self.block_df)
        self.block_colors = self._color_blocks(self.block_neighbors)
        self.colored_blocks = []
        for b in blocks:
            b2 = b.copy()
            b2['color'] = self.block_colors[b['id']]
            self.colored_blocks.append(b2)

    def _neighbors_for_block(self, block, df):
        same_x =  df[(df['x'] == block['x'])]
        higher = same_x['y0'] == block['y1']
        lower = same_x['y1'] == block['y0']
        y_neighbors = same_x[higher | lower].index.tolist()

        one_off = df[(df['x'] - block['x']).abs() == 1]
        higher = one_off['y0'] >= block['y1']
        lower = one_off['y1'] <= block['y0']
        overlap = (higher | lower) == False
        x_neighbors = one_off[overlap].index.tolist()

        neighbors = x_neighbors + y_neighbors
        return neighbors

    def _blocks_to_graph(self, df):
        neighbors = {}
        for i, block in df.iterrows():
            neighbors[i] = self._neighbors_for_block(block, df)

        a = pd.Series(neighbors)
        b = pd.Series({k:len(v) for k,v in a.items()})
        sorted_neighbors = a[b.sort_values(ascending=False).index]
        return sorted_neighbors


    def _color_blocks(self, bneighbors):
        block_colors = pd.Series(index=bneighbors.index)
        for block_id, neighbors in bneighbors.items():
            taken_colors = block_colors.loc[neighbors]
            available_colors = list(self.c2 - set(taken_colors))
            if available_colors:
                block_colors[block_id] = random.choice(available_colors)
            else:
                block_colors[block_id] = "yellow"
        return block_colors

    def mpl_patches(self):
        patches = []
        for b in self.colored_blocks:
            p = {'xy': (b['x'], b['y0']), 'height': b['y1'] - b['y0'], 'width': 1}
            if 'color' in b:
                p['color'] = b['color']
            patches.append(p)

        self.patches = patches
        return patches


def blocks_to_mpl(blocks, colors):
    bcp = BlockColorPicker(colors, blocks=blocks)
    patches = bcp.mpl_patches()
    return patches