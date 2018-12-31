
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
      

def plot_galaxy_grid(galaxies, rows, columns, save_loc):
        fig = plt.figure(figsize=(columns * 4, rows * 4))  # x, y order
        gs1 = gridspec.GridSpec(rows, columns, fig)  # rows (y), cols (x) order
        gs1.update(wspace=0.025, hspace=0.025)
        for n in range(rows * columns):
            ax = plt.subplot(gs1[n])
            galaxy = galaxies[n, :, :, :]  # n, x, y, channel, in ML style
            data = galaxy.squeeze()
            ax.imshow(data.astype(np.uint8))
            ax.grid(False)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            # TODO add labels
            # label_str = '{:.2}'.format(label)
            # ax.text(60, 110, label_str, fontsize=16, color='r')
        # plt.tight_layout()
        plt.savefig(save_loc, bbox_inches='tight')
        plt.close()
