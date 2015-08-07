--[[
xls path: example/test.xls
]]--

local hander = {}

local __data__ = {
  [1] = {
      ["game_list"] = {
          "wow",
          "lol",
          1,
          {
              ["1"] = {
                  1,
                  2,
                  3,
                  1000,
                  5,
              },
          },
      },
      ["id"] = 1,
      ["is_man"] = false,
      ["name"] = "hey",
  },
  [2] = {
      ["game_list"] = {
          12313,
          "lol",
          23.1,
      },
      ["id"] = 2,
      ["is_man"] = true,
      ["name"] = "hahaha",
  },
}

function hander.getData()
	return __data__
end

-- ========== custom your code area start ==========
-- ========== custom your code area end ==========


return hander