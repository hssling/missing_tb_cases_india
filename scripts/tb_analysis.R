# High-Quality TB Analysis R Script
# Load data, corrs, reg, ggplot visuals, save PNG/PDF dpi=300

library(readr)
library(dplyr)
library(ggplot2)
library(corrplot)
library(gridExtra)

# Paths
tb_path <- "data/processed/nfhs_rs_tb_merged.csv"
merged <- read_csv(tb_path)

# Key vars (shorten names)
merged <- merged %>%
  mutate(
    stunting = `Children under 5 years who are stunted (height-for-age)18 (%)`,
    underweight = `Children under 5 years who are underweight (weight-for-age)18 (%)`,
    anaemia = `Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)`,
    tobacco_men = `Men age 15 years and above who use any kind of tobacco (%)`,
    sanitation = `Population living in households that use an improved sanitation facility2 (%)`,
    tb_cases = `2023`
  )

# Corrs
cor_df <- cor(merged %>% select(stunting, underweight, anaemia, tobacco_men, sanitation, tb_cases), use = "complete.obs")
cor_df <- as.data.frame(round(cor_df, 3))
write_csv(cor_df, "output/tables/corrs_r.csv")

# Regression
lm_model <- lm(tb_cases ~ underweight + sanitation, data = merged)
summary(lm_model)
r2 <- summary(lm_model)$r.squared
coef_df <- data.frame(
  predictor = names(lm_model$coefficients)[-1],
  coef = lm_model$coefficients[-1],
  r2 = r2
)
write_csv(coef_df, "output/tables/reg_r.csv")

# Plots (high quality)
p1 <- ggplot(merged, aes(x = underweight, y = tb_cases)) +
  geom_point() +
  geom_smooth(method = "lm") +
  labs(title = "TB Cases vs Underweight", x = "Underweight %", y = "TB Cases 2023") +
  theme_minimal()

p2 <- ggplot(cor_df %>% filter(row == "tb_cases"), aes(x = reorder(colnames(cor_df)[-6], value), y = value)) +
  geom_col() +
  labs(title = "Correlations with TB Cases", x = "Indicator", y = "r") +
  theme_minimal()

ggsave("output/figures/corr_bar_r.png", p2, dpi = 300, width = 10, height = 6)
ggsave("output/figures/tb_underweight_r.png", p1, dpi = 300, width = 10, height = 6)

# Heatmap
png("output/figures/corr_heatmap_r.png", width = 800, height = 600, res = 300)
corrplot(cor_df, method = "color", type = "upper", order = "hclust")
dev.off()

print("R analysis complete. Files saved.")
