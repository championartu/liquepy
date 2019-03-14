import matplotlib.pyplot as plt
from matplotlib import patches as mpatches


def add_ic_colours(subplot):
    ic_limits = [0, 1.3, 1.8, 2.1, 2.6, 5]

    # Colors
    gravel = [154 / 255, 176 / 255, 187 / 255]
    clean_sand = [255 / 255, 246 / 255, 187 / 255]
    sand_w_fc = [218 / 255, 196 / 255, 77 / 255]
    silty_sand = [223 / 255, 220 / 255, 151 / 255]
    clay_silt = [196 / 255, 148 / 255, 73 / 255]

    colours = [gravel, clean_sand, sand_w_fc, silty_sand, clay_silt,
               (1, 1, 1)]

    gravel_patch = mpatches.Patch(color=gravel, label='Gravel')

    clean_sand_patch = mpatches.Patch(color=clean_sand, label='Clean Sand')

    silty_sand_patch = mpatches.Patch(color=silty_sand, label='Silty Sand')

    sand_w_fc_patch = mpatches.Patch(color=sand_w_fc, label='Sand with much Fines Content')

    clay_silty_patch = mpatches.Patch(color=clay_silt, label='Clay-Silty/Not Liquefable')

    # subplot.rc('legend', fontsize=9)
    subplot.legend([gravel_patch, clean_sand_patch, silty_sand_patch, sand_w_fc_patch, clay_silty_patch,
                (gravel_patch, clean_sand_patch, silty_sand_patch, sand_w_fc_patch, clay_silty_patch)],
               ["Gravel", "Clean Sand", "Silty Sand", "Sand with FC", "Clay-Silty/\nNot Liq.", ], loc=0, prop={"size": 8})

    for i in range(len(ic_limits) - 1):
        subplot.axvspan(ic_limits[i], ic_limits[i + 1], alpha=1.0, color=colours[i])


def make_ic_plot(subplot):
    add_ic_colours(subplot)
    subplot.set_xlim([0, 3])


def make_factor_of_safety_plot(subplot):
    # add the Fs = 1 line
    subplot.axvspan(0, 1.0, alpha=0.5, color="r")
    subplot.axvspan(1.0, 1.25, alpha=0.5, color=(1, 0.6, 0.2))
    subplot.axvspan(1.25, 1.5, alpha=0.5, color=(0.95, 1, 0.4))
    subplot.axvspan(1.5, 2.0, alpha=0.5, color=(0.2, 0.8, 0.2))
    subplot.set_xlim([0, 2.1])


def make_cpt_plots(sps, cpt):

    sps[0].plot(cpt.q_c, cpt.depth, lw=1, c="gray")
    sps[1].plot(cpt.f_s, cpt.depth, lw=1, c="gray")
    sps[2].plot(cpt.u_2, cpt.depth, lw=1, c="gray")
    sps[2].axhline(cpt.gwl, c="k", ls="--", lw=0.7)

    # Prepare y-axis
    ylim = sps[0].get_ylim()
    sps[0].set_ylim([0, ylim[1]])
    sps[0].invert_yaxis()

    # Prepare x-axis
    xlim = sps[0].get_xlim()
    sps[0].set_xlim([0, xlim[1]])
    xlim = sps[1].get_xlim()
    sps[1].set_xlim([0, xlim[1]])
    xlim = sps[2].get_xlim()
    sps[2].set_xlim([0, xlim[1]])

    sps[0].set_ylabel("Depth [m]")
    sps[0].set_xlabel("q_c [kPa]")
    sps[1].set_xlabel("f_s [kPa]")
    sps[2].set_xlabel("u_2 [kPa]")
    plt.tight_layout()


def make_bi2014_outputs_plot(sps, bi2014):

    sps[0].plot(bi2014.pore_pressure, bi2014.depth, lw=1, c="b", label="Pore pressure")
    sps[0].plot(bi2014.sigma_v, bi2014.depth, lw=1, c="r", label="$\sigma_{v}$")
    sps[0].plot(bi2014.sigma_veff, bi2014.depth, lw=1, c="gray", label="$sigma_{v,eff}$")
    sps[0].legend(prop={"size": 8}, loc="lower left")
    sps[0].set_xlabel("Stress [kPa]")

    sps[1].plot(bi2014.i_c, bi2014.depth, "o", lw=1, c="k", alpha=0.5, ms=2)
    make_ic_plot(sps[1])
    # sps[1].legend()
    sps[1].set_xlabel("$I_c$")

    sps[2].plot(bi2014.crr_m7p5, bi2014.depth, "o", lw=1, c="k", alpha=0.5, ms=3)
    sps[2].set_xlabel("$CRR_{m7.5}$")
    sps[2].set_xlim([0, 1.])

    sps[3].plot(bi2014.factor_of_safety, bi2014.depth, "o", lw=1, c="k", alpha=0.5, ms=3)
    make_factor_of_safety_plot(sps[3])
    sps[3].axhline(bi2014.gwl, c="k", ls="--", lw=0.7)
    sps[3].set_xlabel("Factor of Safety")

    # Prepare y-axis
    ylim = sps[0].get_ylim()
    sps[0].set_ylim([0, ylim[1]])
    sps[0].invert_yaxis()

    # Prepare x-axis
    xlim = sps[0].get_xlim()
    sps[0].set_xlim([0, xlim[1]])
    xlim = sps[1].get_xlim()
    sps[1].set_xlim([0, xlim[1]])
    xlim = sps[2].get_xlim()
    sps[2].set_xlim([0, xlim[1]])
    xlim = sps[3].get_xlim()
    sps[3].set_xlim([0, xlim[1]])

    sps[0].set_ylabel("Depth [m]")

    plt.tight_layout()
