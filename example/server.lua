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
      ["is_man"] = false,
      ["id"] = 1,
  },
  [2] = {
      ["game_list"] = {
          [1] = 12313,
          [2] = "lol",
          [3] = 231,
      },
      ["name"] = "hahaha",
      ["is_man"] = true,
      ["id"] = 2,
  },
}

function hander.getData()
	return __data__
end

-- ========== custom your code area start ==========
-- ========== custom your code area end ==========


return hander