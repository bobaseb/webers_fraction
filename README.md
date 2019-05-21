# webers_fraction

A first attempt at implementing Weber's fraction (w) estimation for the model in Halberda, Mazzocco & Feigenson, 2008.

Notice reaction times were not part of this model.

Data input

CSV file should contain variables for subject IDs, stimulus on left, stimulus on right, and if subject responded correctly or not (coded as 0 for incorrect and 1 for correct) with names "ID_subs", "Stim_Left", "Stim_Right", and "Correct_Answer" respectively. This assumes participants had to pick the bigger stimulus for either symbolic or non-symbolic stimuli. Although, Weber's w is probably only informative in the latter case.

Requirements

Numpy, pandas, scipy

Reference

Halberda, J., Mazzocco, M. M., & Feigenson, L. (2008). Individual differences in non-verbal number acuity correlate with maths achievement. Nature, 455(7213), 665.
