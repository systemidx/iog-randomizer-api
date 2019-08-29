using System;
using System.Linq;
using Microsoft.AspNetCore.Http;
using Randomizer.Api.Models;

namespace Randomizer.Api.Extensions
{
    public static class HttpRequestExtensions
    {
        public static IFormFile GetRomFileFromRequest(this HttpRequest request)
        {
            return request?.Form?.Files?.FirstOrDefault();
        }
        
        public static SeedParameters GetParametersFromRequestOrDefault(this HttpRequest request)
        {
            var parameters = new SeedParameters();
            if (request?.Form == null)
                return parameters;

            parameters.Seed = request.ParseLong("seed");
            parameters.Difficulty = request.ParseString("difficulty");
            parameters.Goal = request.ParseString("goal");
            parameters.Statues = request.ParseString("statues");
            parameters.StartPosition = request.ParseString("startLocation");
            parameters.Logic = request.ParseString("logic");
            parameters.AllowGlitches = request.ParseBool("allowGlitches");
            parameters.OneHitKnockOut = request.ParseBool("oneHitKnockOut");
            parameters.RedJewelMadness = request.ParseBool("redJewelMadness");
            parameters.Firebird = request.ParseBool("firebird");
            parameters.Enemizer = request.ParseString("enemizer");
            parameters.BossShuffle = request.ParseBool("bossShuffle");
            parameters.EntranceShuffle = request.ParseString("entranceShuffle");
            parameters.DungeonShuffle = request.ParseBool("dungeonShuffle");
            parameters.OverworldShuffle = request.ParseBool("overworldShuffle ");
            
            return parameters;
        }

        private static string ParseString(this HttpRequest request, string key)
        {
            if (request.Form.ContainsKey(key))
                return request.Form[key];
            
            var parameters = new SeedParameters();
            var type = parameters.GetType().GetProperty(key);

            if (type == null)
                return default;

            return type.GetValue(parameters) as string;
        }

        private static bool ParseBool(this HttpRequest request, string key)
        {
            if (request.Form.ContainsKey(key))
                if (bool.TryParse(request.Form[key], out var result))
                    return result;
            
            var parameters = new SeedParameters();
            var type = parameters.GetType().GetProperty(key);

            if (type == null)
                return default;

            return (bool)type.GetValue(parameters);
        }

        private static long ParseLong(this HttpRequest request, string key)
        {
            if (request.Form.ContainsKey(key))
                if (long.TryParse(request.Form[key], out var result))
                    return result;
            
            var parameters = new SeedParameters();
            var type = parameters.GetType().GetProperty(key);

            if (type == null)
                return default;

            return (long)type.GetValue(parameters);
        }
    }
}
