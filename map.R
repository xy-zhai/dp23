#library --------------
library(ggplot2) #plot
library(sp) #coordinate
library(sf) # classes and functions for vector data
library(raster) #geographic data analysis and modeling
library(broom) # make spatial obj into data frame
library(stringr) # string manipulation 
library(scales) # scales(number format) for ggplot2
library(terra)         # classes and functions for raster data
library(spData)        # load geographic data
#library(spDataLarge)   # load larger geographic data


#download geo data from GADM ----
#jpn1 <- getData("GADM", country = "JPN", level = 1) # ken
jpn2 <- getData("GADM", country = "JPN", level = 2) # town/city
#class(jpn1)
class(jpn2)
#View(jpn2)
#jpn2@data[["NAME_2"]];#eng town/city names
#jpn2@data[['NL_NAME_2']];#jpn town/city names
#plot(jpn2);#jpn maw

#make jpn2 data as sf data frame
#jpn2_df <- tidy(jpn2, region = "NAME_2" ) no use!
#sp tidiers are now soft-deprecated in favor of sf::st_as_sf(),
jpn2_df <- sf::st_as_sf(jpn2)
class(jpn2_df)
head(jpn2_df)
#plot(jpn2_df) #sf objects can be plotted quickly with the function plot()
#View(jpn2_df)


#my-----------
mysf <- jpn2_df[c("NL_NAME_1", "NL_NAME_2")]
head(mysf)
#plot(mysf)

cpi <- read.csv("mycpicity.csv", header = TRUE, sep = ",")
head(cpi)


#world_coffee = left_join(world, coffee_data) may also work
#merge cpi and mysf
cpi_sf <- merge(mysf, cpi, by.x = "NL_NAME_2", by.y = "地域",
                all.x = TRUE #extra rows will be added to the output, one for each row in x that has no matching row in y
)
head(cpi_sf)
names(cpi_sf)
colname <- c("NL_NAME_2","NL_NAME_1", "総合", "食料", "住居", "光熱.水道", "家具.家事用品", "被服及び履物", "保健医療", "交通.通信", "教育", "教養娯楽", "諸雑費")
cpi_sf <- cpi_sf[colname]
head(cpi_sf)

#transform coordinate to point data-----
citynames <- cpi_sf$NL_NAME_2[!is.na(cpi_sf$総合)]
length(citynames)
head(citynames)
# Calculate the centroid for each MULTIPOLYGON
centroids <- st_centroid(cpi_sf[cpi_sf$NL_NAME_2 %in% citynames,])
# Extract the coordinates of the centroids
coords <- st_coordinates(centroids)
class(coords)
# Create a data frame with the coordinates
coords_df <- cbind(centroids, coords)
coords_df <- as.data.frame(coords_df)


#add city names
png("figure4.png", width = 1500, height = 1500, res = 300)
fig4 <-
ggplot() + 
  geom_sf(data = cpi_sf, 
          aes(fill = 総合)) +
  scale_fill_viridis_c(option = "plasma") + #with color bar
  coord_sf() +
  theme_minimal() +
  theme(legend.position = "bottom") +
  labs(title = "CPI in Japan for Dec, 2023 (All items)",
       fill = "CPI") +
  geom_text(data = coords_df, 
            aes(x = X, y = Y, label = NL_NAME_2, color =総合 ), 
            size = 2, fontface = "bold", 
            #color = "Black",
            check_overlap = T) + #allow overlapping
  scale_color_viridis_c(option = "plasma", end = 0.9, guide = 'none')  # no color bar
print(fig4)
dev.off()

