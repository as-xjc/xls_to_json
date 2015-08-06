--[[
xls path: example/test.xls
]]--

local hander = {}

local __data__ = {
  [1] = {
      ["game_list"] = {
          [1] = "wow",
          [2] = "lol",
          [3] = 1,
          [4] = {
              ["1"] = {
                  [1] = 1,
                  [2] = 2,
                  [3] = 3,
                  [4] = 1000,
                  [5] = 5,
              },
          },
      },
      ["name"] = "hey",
      ["id"] = 1,
      ["is_man"] = false,
  },
  [2] = {
      ["game_list"] = {
          [1] = 12313,
          [2] = "lol",
          [3] = 23.1,
      },
      ["name"] = "hahaha",
      ["id"] = 2,
      ["is_man"] = true,
  },
}

function hander.getData()
	return __data__
end

-- ========== custom your code area start ==========
-- ========== custom your code area end ==========


return hander