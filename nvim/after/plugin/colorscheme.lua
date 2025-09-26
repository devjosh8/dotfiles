-- Lua
require('onedark').setup {
    style = 'darker',
    transparent = true
}
require('onedark').load()

vim.api.nvim_set_hl(0, "Visual", { bg = "#555555", fg = "NONE" })
