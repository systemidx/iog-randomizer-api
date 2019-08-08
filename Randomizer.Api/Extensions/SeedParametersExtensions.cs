using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Query.Expressions;
using Randomizer.Api.Models;
using System.Text;

namespace Randomizer.Api.Extensions
{
    public static class SeedParametersExtensions
    {
        public static string GenerateFilenameScheme(this SeedParameters parameters, string version, long seed)
        {
            //IoGR_v1.5.0_Hard_RJ_B_OHKO_191814
            
            string mode;
            switch (parameters.Mode)
            {
                case "Completable":
                    mode = "C";
                    break;

                case "Beatable":
                    mode = "B";
                    break;

                case "Chaos":
                    mode = "X";
                    break;

                default:
                    mode = "Z";
                    break;
            }

            string statues = "DG";
            switch (parameters.Statues)
            {
                case "0":
                    statues = "DG0";
                    break;

                case "1":
                    statues = "DG1";
                    break;

                case "2":
                    statues = "DG2";
                    break;

                case "3":
                    statues = "DG3";
                    break;

                case "4":
                    statues = "DG4";
                    break;

                case "5":
                    statues = "DG5";
                    break;

                case "6":
                    statues = "DG6";
                    break;

                case "Random":
                    statues = "DGR";
                    break;
            }

            var builder = new StringBuilder();
            builder.Append("IoGR");
            builder.Append($"_v{version}");
            builder.Append($"_{parameters.Difficulty}");
            builder.Append(parameters.Goal == "Dark Gaia" ? $"_{statues}": "_RJ");
            builder.Append($"_{mode}");
            if (parameters.Variations != "None")
                builder.Append($"_{parameters.Variations}");
            builder.Append($"_{seed}");

            return builder.ToString();
        }
    }
}