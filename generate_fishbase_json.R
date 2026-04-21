library(rfishbase)
library(jsonlite)

df <- species()

clean_data <- data.frame(
    scientific_name = paste(df$Genus, df$SpeciesRefNo),
    common_name = df$FBname,
    family = df$FamCode,
    max_length_cm = df$Length,
    depth_shallow = df$DepthRangeShallow,
    depth_deep = df$DepthRangeDeep,
    is_marine = df$Saltwater,
    is_freshwater = df$Fresh,
    habitat_type = df$DemersPelag,
    stringAsFactors = FALSE
)

clean_data <- clean_data[!is.na(clean_data$scientific_name), ]

write_json <- toJSON(clean_data, pretty = TRUE, na = "null")

write(write_json, file = "fish_data.json")

print(paste("Saved", nrow(clean_data), "species"))