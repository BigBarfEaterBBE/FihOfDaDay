library(rfishbase)
library(jsonlite)

species_df <- species()
taxonomy_df <- load_taxa()

get_water_type <- function(fresh,salt) {
    "
    Helper function to determine the water type of the fish
    "
    if (is.na(salt) & is.na(fresh)) return(NA)
    if (salt == 1 & (is.na(fresh) | fresh == 0)) return("marine")
    if (fresh == 1 & (is.na(salt) | salt == 0)) return("freshwater")
    return("mixed")
}

species_df <- merge(
    species_df,
    taxonomy_df[, c("SpecCode", "Species")],
    by = "SpecCode",
    all.x = TRUE
)

clean_data <- data.frame(
    scientific_name = species_df$Species,
    common_name = species_df$FBname,
    max_length_cm = species_df$Length,
    depth_shallow = species_df$DepthRangeShallow,
    depth_deep = species_df$DepthRangeDeep,
    water_type = mapply(get_water_type, species_df$Fresh, species_df$Saltwater),
    stringsAsFactors = FALSE
)

# Remove missing names
clean_data <- clean_data[
  !is.na(clean_data$scientific_name) &
  clean_data$scientific_name != "" &
  !is.na(clean_data$common_name) &
  clean_data$common_name != "",
]

# Build depth range 
clean_data$depth_range_m <- ifelse(
  is.na(clean_data$depth_shallow) & is.na(clean_data$depth_deep),
  NA,
  paste(
    ifelse(is.na(clean_data$depth_shallow), "?", clean_data$depth_shallow),
    "-",
    ifelse(is.na(clean_data$depth_deep), "?", clean_data$depth_deep)
  )
)

# Remove rows with null depth
clean_data <- clean_data[!is.na(clean_data$depth_range_m), ]

# Remove rows with null max length
clean_data <- clean_data[!is.na(clean_data$max_length_cm), ]

# Final dataset
final_data <- data.frame(
  scientific_name = clean_data$scientific_name,
  common_name = clean_data$common_name,
  water_type = clean_data$water_type,
  depth_range_m = clean_data$depth_range_m,
  max_length_cm = clean_data$max_length_cm,
  stringsAsFactors = FALSE
)

# Export
write(toJSON(final_data, pretty = TRUE, na = "null"),
      file = "fish_data_clean.json")

print(paste("Clean dataset saved:", nrow(final_data), "species"))