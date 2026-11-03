"""The Omelyan-Trotter scheme collection."""

from .omelyan_trotter import OmelyanTrotter


class Leapfrog2(OmelyanTrotter):
    r"""Second-order leapfrog (Verlet) scheme [1].

    This is the standard second-order symmetric product formula with a single cycle.
    It corresponds to the Omelyan-Trotter scheme with ``c_vec = [0.5]``,
    and generates the following product:

    .. math::

        e^{(A + B) h + \mathcal{O} (h^3)} = e^{A/2} e^{B} e^{A/2}.

    Considering its simplicity, it performs well in cases where high precision is
    not explicitly desired.

    References:
        [1]: L. Verlet, "Computer "Experiments" on Classical Fluids. I.
             Thermodynamical Properties of Lennard–Jones Molecules", Phys. Rev.,
             vol. 159, pp. 98-103, 1 1967.
             DOI: `10.1103/PhysRev.159.98 <https://doi.org/10.1103/PhysRev.159.98>`_

    See also:
        OmelyanTrotter
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 2
        cycles = 1
        c_vec = [0.5]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Omelyan2(OmelyanTrotter):
    r"""Second-order Omelyan improved scheme [1].

    This is the Omelyan improved second-order Trotter scheme with two cycles.
    It corresponds to the Omelyan-Trotter scheme with
    ``c_vec = [0.193183327503770311, 0.306816672496229689]``

    Omelyan et al. derived an improved second-order formula, with a higher
    theoretical efficiency.
    In practice however, it usually performs similarly well as the Leapfrog scheme.

    References:
        [1]: I. Omelyan, I. Mryglod and R. Folk,
             "Optimized Forest–Ruth- and Suzuki-like Algorithms for Integration
             of Motion in Many-body Systems", Computer Physics Communications,
             vol. 146, no. 2, pp. 188-202, 2002.
             DOI: `10.1016/s0010-4655(02)00451-4 <https://doi.org/10.1016/s0010-4655(02)00451-4>`_

    See also:
        OmelyanTrotter
        Leapfrog2
        Omelyan4
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 2
        cycles = 2
        c_vec = [0.193183327503770311, 0.306816672496229689]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Forest_Ruth4(OmelyanTrotter):
    r"""Fourth-order Forest-Ruth product formula [1].

    This is the first fourth-order Trotter scheme, which was derived
    by Forest and Ruth.
    In our notation it has 3 cycles and corresponds to
    the Omelyan-Trotter scheme with
    ``c_vec = [0.675603595979828817, -0.851207191959657634, 0.675603595979828816]``

    It is the least efficient scheme at order n = 4, and the simplest example of
    Suzuki's higher order scheme construction.
    In practice, it can perform worse than the Leapfrog for a small enough
    number of repetitions.

    References:
        [1]: E. Forest and R. D. Ruth, "Fourth-order Symplectic Integration",
             Physica D: Nonlinear Phenomena, vol. 43, no. 1, pp. 105-117, 1990.
             DOI: `10.1016//0167-2789(90)90019-L <https://doi.org/10.1016/0167-2789(90)90019-L>`_

    See also:
        OmelyanTrotter
        Leapfrog2
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 4
        cycles = 3
        c_vec = [0.675603595979828817, -0.851207191959657634, 0.675603595979828816]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Omelyan4(OmelyanTrotter):
    r"""Fourth-order Omelyan's improved Forest-Ruth scheme [1].

    This is the Omelyan improved fourth-order Trotter scheme with four cycles.
    Adding a cycle to Forest-Ruth an emergent free parameter can be optimized.
    The resulting scheme is more efficient than the one by Forest and Ruth,
    but is outshone by schemes at higher cycles within order n = 4.

    References:
        [1]: I. Omelyan, I. Mryglod and R. Folk,
             "Optimized Forest–Ruth- and Suzuki-like Algorithms for Integration
             of Motion in Many-body Systems", Computer Physics Communications,
             vol. 146, no. 2, pp. 188-202, 2002.
             DOI: `10.1016/s0010-4655(02)00451-4 <https://doi.org/10.1016/s0010-4655(02)00451-4>`_

    See also:
        OmelyanTrotter
        Omelyan2
        Forest_Ruth4
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 4
        cycles = 4
        c_vec = [
            0.172086508927428834,
            -0.581097833373203791,
            0.489536610172273414,
            0.419474714273501542,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Malezic_Ostmeyer4(OmelyanTrotter):
    r"""Fourth-order maximal cycles scheme with improved efficiency,
    found by Maležič and Ostmeyer [1].

    This is the Omelyan improved fourth-order Trotter scheme with six cycles.
    At order n = 4, the number of cycles q = 6 is maximal, and produces
    the most efficient schemes theoretically.

    In practice, other factors affect the scheme performance, e.g. the distance
    from the origin point, which was taken into account when choosing this scheme.
    For this reason, this scheme has the second highest theoretical efficiency,
    but is expected to perform better in practice.

    References:
        [1]: M. Maležič and J. Ostmeyer, "Efficient Trotter–Suzuki Schemes
             for Long-Time Quantum Dynamics", Journal of Physics A: Mathematical and
             Theoretical 59, 345301 (2026)
             DOI: `10.1088/1751-8121/ae919f <https://doi.org/10.1088/1751-8121/ae919f>`_

    See also:
        OmelyanTrotter
        Malezic_Ostmeyer4_minimal
        Malezic_Ostmeyer6
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 4
        cycles = 6
        c_vec = [
            0.074082572180463262,
            0.232923088374338803,
            0.296820560634668408,
            0.122086989386933251,
            -0.350153632343424469,
            0.124240421767020743,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Malezic_Ostmeyer4_minimal(OmelyanTrotter):
    r"""Fourth-order maximal cycles scheme with minimal distance from the origin,
    found by Maležič and Ostmeyer [1].

    This is the Omelyan improved fourth-order Trotter scheme with six cycles.
    At order n = 4, the number of cycles q = 6 is maximal, and produces
    the most efficient schemes theoretically.

    In practice, other factors affect the scheme performance, e.g. the distance
    from the origin point, which was taken into account when choosing this scheme.
    This scheme has the lowest distance from the origin at q = 6 cycles, which
    comes at a cost of decreased efficiency.

    References:
        [1]: M. Maležič and J. Ostmeyer, "", 2026.
             `arXiv:quant-ph/ <https://arxiv.org/abs/>`_

    See also:
        OmelyanTrotter
        Malezic_Ostmeyer4
        Malezic_Ostmeyer6_minimal
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 4
        cycles = 6
        c_vec = [
            0.287834613619764812,
            0.151098631207585238,
            0.154721182891605497,
            0.112757707574057481,
            0.117761677709795246,
            -0.324173813002808231,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Yoshida6(OmelyanTrotter):
    r"""Sixth-order minimal cycles Yoshida scheme [1].

    This is the first sixth-order scheme at minimal cycles q = 7.
    It was derived by Yoshida using his construction method, besides two
    other schemes, which are much less efficient.
    The scheme itself is also highly inefficient compared to other schemes
    at order n = 6, and should not be used in practice.

    References:
        [1]: H. Yoshida, "Construction of higher order symplectic integrators",
             Physics Letters A, vol. 150, no. 5, pp. 262-268, 1990.
             DOI: `10.1016/0375-9601(90)90092-3 <https://doi.org/10.1016/0375-9601(90)90092-3>`_

    See also:
        OmelyanTrotter
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 6
        cycles = 7
        c_vec = [
            0.392256805238778632,
            0.117786606679679069,
            -0.588839992089435503,
            0.657593160341955605,
            -0.588839992089435498,
            0.117786606679679063,
            0.392256805238778632,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Blanes_Moan6(OmelyanTrotter):
    r"""Sixth-order improved scheme found by Blanes and Moan [1].

    This is the sixth-order scheme at q = 10 cycles proposed by
    Blanes and Moan.
    It is much more efficient than the sixth-order scheme derived by Yoshida,
    and therefore a good choice at order n = 6.
    However, it does not utilize the maximal number of cycles at this order,
    and is theoretically not the most efficient.

    References:
        [1]: S. Blanes and P. Moan, "Practical Symplectic Partitioned Runge–Kutta
             and Runge–Kutta–Nyström Methods", Journal of Computational
             and Applied Mathematics, vol. 142, no. 2, pp. 313-330, 2002.
             DOI: `10.1016/S0377-0427(01)00492-7 <https://doi.org/10.1016/S0377-0427(01)00492-7>`_

    See also:
        OmelyanTrotter
        Yoshida6
        Malezic_Ostmeyer6
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 6
        cycles = 10
        c_vec = [
            0.050262764400392200,
            0.314960616927694200,
            0.492426372489875900,
            0.237063913978121900,
            0.346358189850726900,
            -0.362762779254344799,
            0.195602488600053199,
            -0.425118767797690800,
            -0.447346482695478100,
            0.098553683500649899,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Malezic_Ostmeyer6(OmelyanTrotter):
    r"""Sixth-order maximal cycles scheme with improved efficiency,
    found by Maležič and Ostmeyer [1].

    This is the Omelyan improved sixth-order Trotter scheme with fourteen cycles.
    At order n = 6, the number of cycles q = 14 is maximal, and produces
    the most efficient schemes theoretically.

    In practice, other factors affect the scheme performance, e.g. the distance
    from the origin point, which was taken into account when choosing this scheme.
    For this reason, this scheme has the second highest theoretical efficiency,
    but is expected to perform much better in practice.

    References:
        [1]: M. Maležič and J. Ostmeyer, "Efficient Trotter–Suzuki Schemes
             for Long-Time Quantum Dynamics", Journal of Physics A: Mathematical and
             Theoretical 59, 345301 (2026)
             DOI: `10.1088/1751-8121/ae919f <https://doi.org/10.1088/1751-8121/ae919f>`_

    See also:
        OmelyanTrotter
        Malezic_Ostmeyer4
        Malezic_Ostmeyer6_minimal
        Malezic_Ostmeyer8_q21
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 6
        cycles = 14
        c_vec = [
            0.037251326545569924,
            0.120600278793781562,
            0.266062994460763541,
            0.163668553338143183,
            0.071316838327437583,
            0.058117508592333414,
            0.188707697234255120,
            -0.200016005078878524,
            0.074145714537530386,
            0.087345801243357893,
            0.044234977360777830,
            -0.230821838291030424,
            -0.237197828922049295,
            0.056583981858007803,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Malezic_Ostmeyer6_minimal(OmelyanTrotter):
    r"""Sixth-order maximal cycles scheme with uniformity,
    found by Maležič and Ostmeyer [1].

    This is the Omelyan improved sixth-order Trotter scheme with fourteen cycles.
    At order n = 6, the number of cycles q = 14 is maximal, and produces
    the most efficient schemes theoretically.

    In practice, other factors affect the scheme performance, e.g. the distance
    from the origin point, which was taken into account when choosing this scheme.
    This scheme has the lowest distance from the origin at q = 14 cycles, which
    comes at a cost of decreased efficiency.

    References:
        [1]: M. Maležič and J. Ostmeyer, "", 2026.
             `arXiv:quant-ph/ <https://arxiv.org/abs/>`_

    See also:
        OmelyanTrotter
        Malezic_Ostmeyer4_minimal
        Malezic_Ostmeyer6
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 6
        cycles = 14
        c_vec = [
            0.043704135948876253,
            0.085971959351543434,
            -0.140210973528653471,
            0.235739169767919005,
            0.098175286900802475,
            0.094535865815963044,
            0.078981222193509087,
            0.068583665915761011,
            0.082485694645635016,
            -0.165420520751213745,
            -0.226675480808975371,
            0.057382351788547323,
            0.108345004651375282,
            0.078402618108910652,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Morales8(OmelyanTrotter):
    r"""Eighth-order scheme derived by Morales et al. [1],
    by following Yoshida's method [2].

    This is one of the solutions for an order n = 8 scheme given by Morales et al.
    Yoshida already derived some eighth-order schemes, but this one outperforms them
    by orders of magnitude. Due to it's improved scaling, it performs well, but can be
    outdone by some sixth-order schemes at a smaller number of steps.

    References:
        [1]: M. E. S. Morales, P. C. S. Costa, D. K. Burgarth, Y. R. Sanders
             and D. W. Berry, "Greatly improved higher-order product formulae
             for quantum simulation", 2022.
             `arXiv:quant-ph/2210.15817 <https://arxiv.org/abs/2210.15817>`_
        [2]: H. Yoshida, "Construction of higher order symplectic integrators",
             Physics Letters A, vol. 150, no. 5, pp. 262-268, 1990.
             DOI: `10.1016/0375-9601(90)90092-3 <https://doi.org/10.1016/0375-9601(90)90092-3>`_

    See also:
        OmelyanTrotter
        Morales10
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 8
        cycles = 17
        c_vec = [
            0.063916804931420539,
            0.280744226331782243,
            -0.192002866507456979,
            0.079913811043049626,
            -0.200245552140900553,
            0.093348240747703450,
            0.130101971174520761,
            0.145686923839933300,
            -0.302927118840104760,
            0.145686923839933298,
            0.130101971174520761,
            0.093348240747703449,
            -0.200245552140900555,
            0.079913811043049619,
            -0.192002866507456983,
            0.280744226331782242,
            0.063916804931420539,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Malezic_Ostmeyer8_q21(OmelyanTrotter):
    r"""Eighth-order efficient Yoshida-type composite scheme at q = 21 cycles,
    found by Maležič and Ostmeyer [1].

    This is the Omelyan improved eighth-order Trotter scheme with twenty-one cycles.
    In this region of cycles only composite schemes of Yoshida-type are allowed,
    and this scheme is the most efficient in this region, with a small distance
    from the origin, making it a good candidate as a general product formula.

    References:
        [1]: M. Maležič and J. Ostmeyer, "", 2026.
             `arXiv:quant-ph/ <https://arxiv.org/abs/>`_

    See also:
        OmelyanTrotter
        Malezic_Ostmeyer6
        Malezic_Ostmeyer8_q21_minimal
        Malezic_Ostmeyer8_q25
        Malezic_Ostmeyer8_q30
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 8
        cycles = 21
        c_vec = [
            0.041644811759980006,
            0.082401316690625129,
            -0.100053679877075558,
            0.056276640904364281,
            0.054789293427501641,
            0.052417975744997715,
            0.202143137014514557,
            -0.156387050011859596,
            0.047476878333309942,
            0.077958103121855915,
            -0.217334854216428036,
            0.077958103121855915,
            0.047476878333309942,
            -0.156387050011859596,
            0.202143137014514557,
            0.052417975744997715,
            0.054789293427501641,
            0.056276640904364281,
            -0.100053679877075558,
            0.082401316690625129,
            0.041644811759980006,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Malezic_Ostmeyer8_q21_minimal(OmelyanTrotter):
    r"""Eighth-order Yoshida-type composite scheme at q = 21 cycles,
    found by Maležič and Ostmeyer [1].

    This is the Omelyan improved eighth-order Trotter scheme with twenty-one cycles.
    In this region of cycles only composite schemes of Yoshida-type are allowed,
    and this scheme is the most uniform in this region, with a small distance
    from the origin.

    References:
        [1]: M. Maležič and J. Ostmeyer, "", 2026.
             `arXiv:quant-ph/ <https://arxiv.org/abs/>`_

    See also:
        OmelyanTrotter
        Malezic_Ostmeyer6
        Malezic_Ostmeyer8_q21
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 8
        cycles = 21
        c_vec = [
            0.046821019583626999,
            0.065094747922117141,
            0.179526744281134160,
            -0.123740270767225768,
            -0.119655652043950497,
            0.046873313877776816,
            0.058109443320545039,
            0.063312160977716025,
            0.067101081641059754,
            0.063734886837763863,
            -0.194354951261127062,
            0.063734886837763863,
            0.067101081641059754,
            0.063312160977716025,
            0.058109443320545039,
            0.046873313877776816,
            -0.119655652043950497,
            -0.123740270767225768,
            0.179526744281134160,
            0.065094747922117141,
            0.046821019583626999,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Malezic_Ostmeyer8_q25(OmelyanTrotter):
    r"""Eighth-order Yoshida-type composite scheme at q = 25 cycles,
    found by Maležič and Ostmeyer [1].

    This is the Omelyan improved eighth-order Trotter scheme with twenty-five cycles.
    In this region of cycles only composite schemes of Yoshida-type are allowed,
    and this scheme is one of the most efficient in this region, with a small distance
    from the origin, making it a good candidate as a general product formula.

    References:
        [1]: M. Maležič and J. Ostmeyer, "", 2026.
             `arXiv:quant-ph/ <https://arxiv.org/abs/>`_

    See also:
        OmelyanTrotter
        Malezic_Ostmeyer6
        Malezic_Ostmeyer8_q21
        Malezic_Ostmeyer8_q30
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 8
        cycles = 25
        c_vec = [
            0.035040437439599538,
            0.083654200180512575,
            -0.094441856492887166,
            0.045282684942868918,
            0.042686399911943541,
            0.039337289378021986,
            0.040200947014508506,
            0.189095614596034745,
            -0.147573727016947265,
            0.029161512527994420,
            0.080819932709682712,
            0.008242786742480780,
            -0.203012443867626569,
            0.008242786742480780,
            0.080819932709682712,
            0.029161512527994420,
            -0.147573727016947265,
            0.189095614596034745,
            0.040200947014508506,
            0.039337289378021986,
            0.042686399911943541,
            0.045282684942868918,
            -0.094441856492887166,
            0.083654200180512575,
            0.035040437439599538,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Malezic_Ostmeyer8_q30(OmelyanTrotter):
    r"""Eighth-order generic scheme at q = 30 cycles,
    found by Maležič and Ostmeyer [1].

    This is the Omelyan improved eighth-order Trotter scheme with thirty cycles.
    In this region of cycles generic schemes exist too, which allow for improvements.
    At maximal number of cycles this scheme is highly efficient, and has a low distance
    from the origin. In both respects however, it is worse than the scheme at q = 30 cycles.

    References:
        [1]: M. Maležič and J. Ostmeyer, "", 2026.
             `arXiv:quant-ph/ <https://arxiv.org/abs/>`_

    See also:
        OmelyanTrotter
        Malezic_Ostmeyer6
        Malezic_Ostmeyer8_q21
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 8
        cycles = 30
        c_vec = [
            0.026395999625833815,
            -0.233684379758421046,
            -0.347051470763567071,
            -0.274493109455153539,
            0.061094592879806627,
            0.080452813774411269,
            -0.063568811420699228,
            0.079026700770564284,
            0.059258569653719090,
            0.101028778330863239,
            -0.164724202482292914,
            -0.153554503905898948,
            0.107485850556923307,
            -0.132867087173779791,
            -0.074760981570922924,
            0.153609834123292238,
            0.024200829485005276,
            -0.155771661397294425,
            0.089897001564395437,
            0.185309492367605244,
            0.093200666104659380,
            0.092333475195637504,
            0.050724396546212469,
            0.057234606768893276,
            -0.114753172414141125,
            0.033620005282797918,
            0.217672800411770034,
            0.344599868646588370,
            0.286949675877411436,
            0.071133422375779604,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )


class Morales10(OmelyanTrotter):
    r"""Tenth-order scheme derived by Morales et al. [1],
    by following Yoshida's method [2].

    This is one of the solutions for an order n = 10 scheme given by Morales et al.
    The scaling of this scheme is improved, but it does not necessarily perform
    better than schemes of lower order due to it's low efficiency.

    References:
        [1]: M. E. S. Morales, P. C. S. Costa, D. K. Burgarth, Y. R. Sanders
             and D. W. Berry, "Greatly improved higher-order product formulae
             for quantum simulation", 2022.
             `arXiv:quant-ph/2210.15817 <https://arxiv.org/abs/2210.15817>`_
        [2]: H. Yoshida, "Construction of higher order symplectic integrators",
             Physics Letters A, vol. 150, no. 5, pp. 262-268, 1990.
             DOI: `10.1016/0375-9601(90)90092-3 <https://doi.org/10.1016/0375-9601(90)90092-3>`_

    See also:
        OmelyanTrotter
        Morales8
    """

    def __init__(
        self,
        reps=1,
        merge_single=True,
        merge_steps=True,
        insert_barriers=False,
        cx_structure="chain",
        atomic_evolution=None,
        wrap=False,
        preserve_order=True,
        *,
        atomic_evolution_sparse_observable=False,
    ):
        order = 10
        cycles = 33
        c_vec = [
            0.040603659105128917,
            0.102059372373484241,
            0.333576029136068776,
            0.077073458899788712,
            -0.079218462368935611,
            -0.342772124480309763,
            0.030499570279594295,
            -0.132205995915730353,
            0.065321365348933640,
            0.101094763095369042,
            -0.173114884665614835,
            0.494275937663783538,
            -0.494140660592729350,
            0.173907705343525828,
            0.145215861148504397,
            -0.247250658997780216,
            0.310150129253800483,
            -0.247250658997778264,
            0.145215861148507680,
            0.173907705343526472,
            -0.494140660592732433,
            0.494275937663780444,
            -0.173114884665617632,
            0.101094763095363679,
            0.065321365348932828,
            -0.132205995915731028,
            0.030499570279623287,
            -0.342772124480303955,
            -0.079218462368930145,
            0.077073458899794397,
            0.333576029136074380,
            0.102059372373477402,
            0.040603659105131142,
        ]
        super().__init__(
            order=order,
            cycles=cycles,
            c_vec=c_vec,
            reps=reps,
            merge_single=merge_single,
            merge_steps=merge_steps,
            insert_barriers=insert_barriers,
            cx_structure=cx_structure,
            atomic_evolution=atomic_evolution,
            wrap=wrap,
            preserve_order=preserve_order,
            atomic_evolution_sparse_observable=atomic_evolution_sparse_observable,
        )