# Future avenues for precision oscillation measurements with compact movable reactors

- Authors: M. Hostert, S. A. Meighen-Berger, M. Pospelov
- arXiv: 2611.26418
- Venue: preprint
- INSPIRE: https://inspirehep.net/literature/3231416

## Abstract

No planned neutrino experiment is expected to surpass Daya Bay's precision on $\thone$. Doing so requires innovative strategies to reduce statistical and systematic uncertainties. In this study, we consider a futuristic program with a movable reactor antineutrino source placed within short distances ($L\lesssim 3\,\km$) from the Jiangmen Underground Neutrino Observatory (JUNO) detector. Due to the large fiducial mass of JUNO, even a relatively small reactor can produce a statistically significant number of events over a few years to probe the $\lesssim 8.7\% \,\nuebar$ disappearance set by $\thone$. We consider two possibilities: a $\mathcal{O}(20\mwth)$ microreactor in alcoves of the access tunnel to the underground laboratory, and a $\mathcal{O}(400 \mwth)$ unit on the surface. In both cases the reactor is observed by a small flux monitor detector near the source, while JUNO measures the antineutrino flux at two baselines, suppressing correlated flux and detector systematics. Using the measured Daya Bay per-isotope spectra and its covariance, we model a high-assay low-enriched uranium (HALEU) core for the microreactor and a low-enriched uranium (LEU) core for the surface unit, and discuss various potential sources of systematic uncertainties and their impact on the precision of $\thone$. The underground microreactor could improve on JUNO's reach by a factor of three to four, to $\relsth \simeq 4\%$ over a decade, while the surface reactor would reach the present global-fit precision, $\relsth=2.5\%$, in about three years, provided the emission rate is monitored across reactor relocations to the sub-percent level.

## Introduction (LaTeX, truncated)

Over two decades after neutrino oscillations were established~, the field has entered an era of precision: the mass-squared differences are known to about $1\%$ and $\sin^2\theta_{ij}$ to a few percent~.
The two remaining unknowns of the three-neutrino picture are the mass ordering (MO) and $\delta_{\rm CP}$.
The MO will be determined by JUNO~ in combination with accelerator~ and atmospheric data~, and independently by DUNE~, while $\delta_{\rm CP}$ will be measured by DUNE and Hyper-Kamiokande~.
With JUNO projected to measure $\sin^2\thtwo$ to better than $0.5\%$~, and DUNE and Hyper-Kamiokande $\sin^2\thtwothree$ to $0.5$–$3\%$, depending on its true value, $\thone$ may very well become the least precisely known mixing angle in the next decade.

The current precision on $\thone$ is dominated by three dedicated multi-detector reactor experiments. 
Daya Bay achieved the world-leading $\sin^2\!2\thone$ constraint using eight approximately identical detectors at near ($\simeq 0.5\,\km$) and far ($\simeq 1.6\,\km$) sites around the Daya Bay and Ling Ao reactors~.
It established
\begin{align}
    \sinsqtwo{\thone} &= 0.0851  \times (1 \pm 2.8\%),
\\
     \frac{\dmee}{10^{-3}\eV^2 } &= 2.519 \times (1 \pm 2.4\%),
\end{align}
where $\Delta m^2_{ee} \equiv \cos^2\theta_{12}\,\Delta m_{31}^2 + \sin^2\theta_{12}\,\Delta m^2_{32}$~.
The RENO experiment used a two-detector configuration at the Hanbit plant in South Korea, reaching a comparable but somewhat smaller sensitivity~.
Double Chooz operated first with a far detector only and later added a near detector using the two Chooz reactors in les Ardennes in France~. 
Global fits currently quote the precision on $\sin^22\thone$ as $2.5\%$ ($1\sigma$)~ and a recent analysis combining Daya Bay data with capture on gadolinium and hydrogen reaches~,
\begin{equation}
    \sin^2(2\thone) = 0.0833 \times ( 1 \pm 2.6\%).
\end{equation} 
JUNO can measure $\thone$, but with a precision that is not competitive with Daya Bay because at $52.5\,\km$ the $\thone$-dependent signal is only a $\lesssim 2\%$ modulation of an already oscillated spectrum, far smaller than the $8.7\%$ dip at the first $\nuebar$ survival minimum at short baselines.
JUNO alone is projected to reach $\relsth \simeq 12\%$ after six years of data taking~.
DUNE and Hyper-Kamiokande will not be competitive either.

There are several benefits to reducing the uncertainty on $\thone$.
Since the leading term of the $\nu_\mu\to\nu_e$ appearance probability scales as $\sin^2\thtwothree\sin^2 2\thone$, an independent $\thone$ measurement improves the octant determination near maximal mixing ($\theta_{23}\simeq \pi/4$).
In addition, comparing reactor and accelerator determinations of $\thone$ tests the unitarity of the leptonic mixing matrix~, and this method may be limited by the reactor uncertainty within a decade.
The smallest factor of the Jarlskog invariant, $J_{\rm CP} = c_{12}s_{12}c_{23}s_{23}c^2_{13}s_{13}\sin\delta_{\rm CP} \simeq 0.033\sin\delta_{\rm CP}$~, is $s_{13}$, so $\sigma(J_{\rm CP})/J_{\rm CP} \supset \sigma(\thone)/\thone$, although a better reactor prior only mildly improves the $\delta_{\rm CP}$ reach of DUNE and Hyper-Kamiokande~.
Finally, $\thone$ has been a key discriminant of flavor-symmetry models, whose sum rules relate it to $\thtwo$, $\thtwothree$ and $\delta_{\rm CP}$~.
Future oscillation measurements will significantly reduce the number of viable flavor models~ and $\thone$ could help narrow down their underlying parameter space further.

Daya Bay was the result of a monumental experimental effort. 
It sampled antineutrinos from six reactor cores of 2.9~$\gwth$ each, using eight identically designed detectors in two near halls and one far hall. 
The near–far arrangement made reactor-flux and fuel-composition uncertainties largely cancel in relative comparisons. 
Each detector contained about 20 tonnes of liquid scintillator with 0.1\% gadolinium doping. 
The collaboration had already observed $\theta_{13}$-driven disappearance at more than $5\sigma$ with about 50 days of data in 2012~, before the full 8-detector setup was even installed. 
It ran for nearly nine years, collecting 3158 days of data between December 2011 and December 2020 and a total of $5.55\times 10^6$ inverse beta decay (IBD) events~.
That the precision in \cref{eq:DayaBay_Gd,eq:DayaBay_H} is not expected to be surpassed by any currently running or approved experiment illustrates both the power of the Daya Bay design and how difficult further improvement of $\theta_{13}$ will be with conventional reactor setups.
Only a few proposals to achieve that exist such as SuperChooz that would utilize the past underground cavern for the dismantled Chooz A reactor in les Ardennes~ and improved scintillation technology for cosmic background rejection explored by the LiquidO project~.
Other more ambitious reactor setups to achieve sub-percent precision have also been recently discussed~.

In this study, we turn to the possibility of using JUNO for an ambitious post-mass-ordering program: monitoring \textit{movable} nuclear-reactor(s) to collect an unprecedented number of IBD and elastic scattering events within a single detector.
In this first study, we explore different compact reactor setups with baselines of $L\simeq 0.2$ to $3\,\km$ as shown in \cref{fig:sketch}.
These can exploit JUNO's large mass ($20\,$kton), excellent energy resolution (${\sim}3\%$ at $1\,\MeV$~), and low-background environment to probe the $L/E$ dependence of atmospheric-frequency $\Delta m^2_{31}$ oscillations.
Due to their proximity, even relatively low-power reactors can overwhelm the signal of JUNO's fixed $\gwth$-scale far reactors.
By moving such reactors, one can invert the strategy of Daya Bay, RENO, and Double Chooz, and cancel correlated flux and spectral systematics by comparing near and far placements of the reactor with a single fixed detector.
Continuous operation of reactors would be preferable, but restarts of the core or replica reactors are more realistic on land and if closely monitored, may also achieve the desired effect.

For this study we focus on two potential configurations with different logistical constraints on reactor power as illustrated in \cref{fig:sketch_2}:
\begin{enumerate}
\item[]\textbf{Configuration~A}: a $\lesssim 20\mwth$ microreactor placed in alcoves of the access tunnel to the underground laboratory (or buried in the surrounding rock), located $0.2 - 1.3\,\km$ from the JUNO detector, offering a measurement of a weakly oscillated spectrum ($0.2\%$ deficit) at the closest location and a maximally-$\thone$-oscillated spectrum at the farthest location.
The $1.3$~km distance is optimal for the statistically-limited regime of a low power reactor.
Small flux monitor detector(s) benefit from the overburden inside the cavern and can calibrate the source normalization across the two locations.

\item[] \textbf{Configuration~B}: a $\lesssim 400\mwth$ reactor placed on the surface, at $0.7$ and $2.1\,\km$ from the detector.
Given the surface placement, the reactor power can be higher than in Configuration~A.
We find that the further far-site $\simeq 2$~km location is optimal for two reasons: i) this configuration is not limited by statistics due to the higher power reactor allowing us to slide the $\nuebar$ survival minimum to higher energies, and ii) no location on the surface would see an unoscillated spectrum, so having a further far-site location maximizes the difference between the near and far reactor $\nuebar$ spectrum.  
Small monitor detector(s) that travel with the reactor can help calibrate the emitted $\nuebar$ flux across stops but would require some overburden to reject cosmic backgrounds.
\end{enumerate}

In a companion paper, we explore other configurations for a fixed compact nuclear reactor source at JUNO without focusing on three-flavor oscillations~.
The logistics of fixed microreactors coupled to large underground detectors is simpler and enables a high-statistics IBD and neutrino-electron scattering program.
In this sense, the oscillation program discussed here is more ambitious and imposes more constraints on the setup than other complementary programs on precision or beyond-the-Standard Model physics with fixed microreactors would.

It is worth noting that the idea of studying neutrinos with a movable reactor is not new: nuclear-powered vessels~, dedicated low-power reactors next to a large detector~, and a mobile sub-$\!\gwth$ source operated at two distances from a $50\,$kt scintillator detector~ have been previously discussed. 
Movable detectors have a longer history still: the same detector was operated at several distances at G\"{o}sgen, Bugey and Rovno in the 1980s~, movable detectors were proposed for cross-calibrating the near and far sites of the $\thone$ experiments~, a movable spectrometer scanning $50 - 1700\,$m from a reactor was proposed for sterile-neutrino searches~, and the same-detector ratio method is now s

## Conclusion (LaTeX, truncated)

The technology of deployable compact reactors is actively being pursued worldwide.
These range from units of few $\mwth$ with typical dimensions of standard containers to small modular reactors of several hundred $\mwth$ that are assembled from prefabricated modules. 
These reactors will be intense deployable antineutrino sources that can be brought close to existing large detectors.
With this in mind, we consider a potential post-mass-ordering program for JUNO involving a deployable compact reactor.

JUNO will establish the mass ordering at $3\sigma$ in about six to eight years~.
The final stretch of this period is likely to bring a greater-than-$5\sigma$ determination from global neutrino data including Hyper-Kamiokande and atmospheric neutrinos~.
It could also coincide with the MO determination at more than $5\sigma$ at DUNE alone through matter effects~.\footnote{For the current status of global constraints on the mass ordering and their caveats~, see Refs.~.}
JUNO can then turn to other physics programs, including a possible upgrade to a neutrinoless double-beta decay experiment~.
Here we discussed another possibility: the deployment of a movable compact reactor either in the access tunnel of the underground laboratory or on the surface above it.
In this first exploratory study, we consider a measurement of $\thone$ and what would be needed to improve on the world-leading Daya Bay's measurement.

Using the Daya Bay \uthirtyfive and \pthirtynine spectra and covariance~ and the Huber-Mueller model for \uthirtyeight and \pfortyone~, we modeled a HALEU core with a simplified fuel evolution model and an LEU core following thr Daya Bay fuel evolution.
For the HALEU core, the high-energy flux component drops by only $\simeq 3\%$ in ten years, in contrast with an $\mathcal{O}(10\%)$ drop for thr 18-month cycle of the LEU core.
We find that Configuration A with a $20\mwth$ microreactor at $0.2$ and $1.3\,\km$ with a $5\,$t monitor, reaches $\relsth \simeq 5.3\%$ after five years and $4.2\%$ after ten.
This reduces to $3.5\%$ for a perfectly reproducible rate, still falling short of Daya Bay's $2.8\%$.
For Configuration B with a $400\mwth$ surface unit at $0.7$ and $2.1\,\km$, with a $20\,$t monitor, we find that JUNO could reach the present global-fit precision of $2.5\%$ in about three years. 
With more exposure, Configuration B could in principle meaningfully improve on Daya Bay's result.
The sensitivity of the near reactor datasets to $\dmee$ would be complementary to that of standalone JUNO, but it cannot improve upon it since the latter probes multiple oscillation cycles, including the interference with the solar mass splitting.

A key requirement for the success of the program proposed here is that the $\nuebar$ emission rate be reproducible, or monitored, to $\simeq 0.1\%$ between stops.
Smooth fuel-evolution distortions are degenerate with the depth of the broad $\thone$ dip (unlike, e.g., the rapid oscillations of eV-scale sterile neutrinos~).
While part of this effect can be controlled by using a near-far-near reactor schedule that brackets the evolution, a flux monitor detector would most likely be critical.
Additional alcoves in Configuration~A, for example, could also provide more baselines and help separate fuel evolution from the $L/E$ dependence of oscillations.
Characterizing the stop-to-stop reproducibility of the emission rate and the achievable shape uncertainty should be the priority for future work in this direction.

Ideally, the reactor would be moving without being turned off.
This would be the case of a reactor mounted on a barge or floating units along a waterway or channel.
In this case, one can genuinely scan the baseline and construct an ``oscillogram" in $L$ and $E_\nu$, mapping the first and even the second $\thone$ oscillation dips.
We are not aware of any waterways around the JUNO location, but if such a channel could be built, a floating unit could deliver a substantial amount of power, such as the one considered in Configuration B.

While at this point in time, the use of several movable microreactor cores may appear futuristic, large industrial investments into affordable/smaller scale nuclear technologies offer well-founded hope for the future. 
After 10+ years of the scheduled JUNO run, these new technologies may become a reality to contemplate the measurement scheme proposed in this paper.
The same sources would enable a program beyond $\thone$, including measuring a large sample of $\bar\nu_e$-electron scattering with $\mathcal{O}(10^5)$ events per 100~MW$\cdot$year, searches for eV-sterile neutrino oscillations, and light new particles produced in nuclear and electromagnetic processes. 
We return to these topics in a future study~.

\begin{acknowledgements}
We thank Stephen Parke for many useful suggestions on this topic. 
We also thank Patrick Huber and Bryce Littlejohn for discussions. 
This work was partially supported by the University of Iowa's Year 2 P3 Strategic 

## Figure candidates

- fig-1.png: fig1_survival_probability.pdf
- fig-2.png: JUNO_diagram.png
- fig-3.png: fig3a_ratio_configA.pdf
- fig-4.png: fig3b_ratio_configB.pdf
- fig-5.png: counts_sources.pdf
- fig-6.png: fig8_experiment_comparison_A.pdf
