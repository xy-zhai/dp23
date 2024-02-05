pkgs <- c('tidyverse','sf', 'sp', 'raster', 'broom', 'stringr', 'scales', 'terra', 'spData')

# Loop through each package
for (pkg in pkgs) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    install.packages(pkg)
    library(pkg, character.only = TRUE)
  }
}

install.packages("spDataLarge", repos = "https://nowosad.r-universe.dev")