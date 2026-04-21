library(rfishbase)
library(jsonlite)

df <- species()

get_water_type <- function(fresh,salt) {
    "
    Helper function to determine the water type of the fish
    "
    if (is.na(salt) & is.na(fresh)) return(NA)
    if (salt == 1 & (is.na(fresh) | fresh == 0)) return("marine")
    if (fresh == 1 & (is.na(salt) | salt == 0)) return("freshwater")
    return("mixed")
}

clean_data <- data.frame(
    scientific_name = paste(df$Genus, df$SpeciesRefNo),
    common_name = df$FBname,
    max_length_cm = df$Length,
    depth_shallow
)