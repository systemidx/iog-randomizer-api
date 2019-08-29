using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using Randomizer.Api.Configuration;
using Randomizer.Api.Models;

namespace Randomizer.Api.Handlers
{
    public class RandomizerHandler
    {
        private readonly RandomizerConfiguration _randomizerConfiguration;

        public RandomizerHandler(RandomizerConfiguration randomizerConfiguration)
        {
            _randomizerConfiguration = randomizerConfiguration;
        }

        public async Task<RandomizerRomCreationDetails> CreateRandomizedRomAsync(UploadedFileDetails uploadedFileDetails, SeedParameters parameters)
        {
            using (var process = new Process())
            {
                var workingDirectory = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
                process.StartInfo = new ProcessStartInfo($"{workingDirectory}\\iogr_rom.exe")
                {
                    Arguments = BuildInvocationArguments(uploadedFileDetails.FullPath, parameters),
                    RedirectStandardError = true,
                    RedirectStandardOutput = true,
                    WorkingDirectory = workingDirectory
                };

                process.Start();
                process.WaitForExit();

                var err = await process.StandardError.ReadToEndAsync();
                var info = await process.StandardOutput.ReadToEndAsync();

                if (err.Length > 0)
                    return new RandomizerRomCreationDetails { Success = false, Output = $"{workingDirectory}\\iogr_rom.exe {BuildInvocationArguments(uploadedFileDetails.FullPath, parameters)}\r\n\n{err}\r\n\n{info}"};

                if (info.IndexOf("ERROR", 0, StringComparison.OrdinalIgnoreCase) > -1)
                    return new RandomizerRomCreationDetails { Success = false, Output = $"{workingDirectory}\\iogr_rom.exe {BuildInvocationArguments(uploadedFileDetails.FullPath, parameters)}\r\n\n{err}\r\n\n{info}"};

                var filename = info.Substring(13);
                filename = filename.Trim('\r', '\n', ' ');

                return new RandomizerRomCreationDetails { Success = true, RomPath = $"{uploadedFileDetails.Directory}//{filename}"};
            }
        }

        public async Task<MemoryStream> GetFileStreamAndDeleteRandomizedRomAsync(UploadedFileDetails uploadedFileDetails, string romPath)
        {
            var ms = new MemoryStream();
            using (var stream = new FileStream(romPath, FileMode.Open, FileAccess.Read))
                await stream.CopyToAsync(ms);

            File.Delete(uploadedFileDetails.FullPath);
            File.Delete(romPath);

            return ms;
        }

        public FileInfo GetSpoilerLog(long seed)
        {
            var directoryInfo = new DirectoryInfo(_randomizerConfiguration.TempStorageDestination);
            var files = directoryInfo.GetFiles($"*{seed}*");
            return !files.Any() ? null : files.First();
        }

        private string BuildInvocationArguments(string path, SeedParameters parameters)
        {
            var builder = new StringBuilder();
            
            builder.Append($"--path {path} ");
            builder.Append($"--seed {parameters.Seed} ");
            builder.Append($"--difficulty \"{parameters.Difficulty}\" ");
            builder.Append($"--goal \"{parameters.Goal}\" ");
            builder.Append($"--logic \"{parameters.Logic}\" ");
            builder.Append($"--enemizer \"{parameters.Enemizer}\" ");
            builder.Append($"--start-pos \"{parameters.StartPosition}\" ");
            builder.Append($"--statues \"{parameters.Statues}\" ");
            builder.Append($"--variant \"{parameters.Variations}\" ");

            return builder.ToString();
        }
    }
}
